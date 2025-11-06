import os
from pathlib import Path
from typing import Dict, List, Optional

import pickle
import numpy as np
import pandas as pd

from .schemas import (
    JugadorEntrada,
    JugadorOportunidad,
    EvaluacionSimpleEntrada,
    JugadorSobreprecio,
)


# Rutas de artefactos del modelo (relativas al proyecto)
_base_dir = Path(__file__).resolve().parents[2]
_models_dir = _base_dir / "models"
_data_dir = _base_dir / "data" / "processed"
_ruta_modelo = _models_dir / "modelo_valoracion_fifa.pkl"
_ruta_columnas = _models_dir / "columnas_modelo.pkl"


# Cache en memoria para evitar recargas repetidas
_modelo = None
_columnas: List[str] = []


def cargar_modelo() -> None:
    """
    Carga el modelo y la lista de columnas desde disco a memoria (cache).

    - Modelo: RandomForestRegressor entrenado
    - Columnas: orden esperado de features por el modelo
    """

    global _modelo, _columnas

    if _modelo is None:
        with open(_ruta_modelo, "rb") as f:
            _modelo = pickle.load(f)

    if not _columnas:
        with open(_ruta_columnas, "rb") as f:
            _columnas = pickle.load(f)


def _calcular_imc(altura_cm: float, peso_kg: float) -> float:
    """Calcula el IMC = peso (kg) / altura (m)^2."""
    altura_m = altura_cm / 100.0
    if altura_m <= 0:
        return np.nan
    return float(peso_kg) / float(altura_m ** 2)


def _fmt_eur_plain(valor: float) -> str:
    """Formatea un valor en euros con separador de miles: €1,234,567."""
    try:
        return f"€{float(valor):,.0f}"
    except Exception:
        return "€0"


def _one_hot_categoricas(posicion_principal: str, pie_preferido: str) -> Dict[str, int]:
    """
    Codifica variables categóricas a one-hot siguiendo las categorías
    presentes en el entrenamiento (modelo_ml.ipynb).
    """

    posiciones = [
        "CAM",
        "CB",
        "CDM",
        "CF",
        "CM",
        "GK",
        "LB",
        "LM",
        "LW",
        "LWB",
        "RB",
        "RM",
        "RW",
        "RWB",
        "ST",
    ]

    pies = ["Left", "Right"]

    features: Dict[str, int] = {}

    # Posición principal
    for p in posiciones:
        features[f"posicion_principal_{p}"] = 1 if posicion_principal == p else 0

    # Pie preferido
    for lado in pies:
        features[f"pie_preferido_{lado}"] = 1 if pie_preferido == lado else 0

    return features


def _alinear_columnas(df: pd.DataFrame, columnas_objetivo: List[str]) -> pd.DataFrame:
    """
    Alinea el DataFrame a `columnas_objetivo`:
    - Agrega columnas faltantes con 0
    - Reordena las columnas
    - Descarta columnas extra
    """

    faltantes = [c for c in columnas_objetivo if c not in df.columns]
    for c in faltantes:
        df[c] = 0

    df = df[columnas_objetivo]
    return df


def preparar_features(entrada: JugadorEntrada) -> pd.DataFrame:
    """
    Construye el vector de features con el mismo esquema usado en el entrenamiento:
    - Numéricas: edad, calificacion_general, potencial, altura_cm, peso_kg, imc, margen_crecimiento
    - Categóricas one-hot: posicion_principal_*, pie_preferido_*
    """

    imc = _calcular_imc(entrada.altura_cm, entrada.peso_kg)
    margen_crecimiento = entrada.potencial - entrada.calificacion_general

    base = {
        "edad": entrada.edad,
        "calificacion_general": entrada.calificacion_general,
        "potencial": entrada.potencial,
        "altura_cm": entrada.altura_cm,
        "peso_kg": entrada.peso_kg,
        "imc": imc,
        "margen_crecimiento": margen_crecimiento,
    }

    ohe = _one_hot_categoricas(
        posicion_principal=entrada.posicion_principal.value,
        pie_preferido=entrada.pie_preferido.value,
    )

    datos = {**base, **ohe}
    df = pd.DataFrame([datos])

    # Alinear al orden esperado por el modelo
    cargar_modelo()
    df = _alinear_columnas(df, _columnas)
    return df


def predecir_valor(entrada: JugadorEntrada) -> float:
    """
    Ejecuta la inferencia y retorna el valor estimado en euros.
    """

    cargar_modelo()
    X = preparar_features(entrada)
    pred = float(_modelo.predict(X)[0])
    return pred


def preparar_features_batch(entradas: List[JugadorEntrada]) -> pd.DataFrame:
    """
    Construye un DataFrame con las features para un lote de jugadores, alineado
    al orden de columnas esperado por el modelo.
    """

    filas = []
    for e in entradas:
        imc = _calcular_imc(e.altura_cm, e.peso_kg)
        margen_crecimiento = e.potencial - e.calificacion_general
        base = {
            "edad": e.edad,
            "calificacion_general": e.calificacion_general,
            "potencial": e.potencial,
            "altura_cm": e.altura_cm,
            "peso_kg": e.peso_kg,
            "imc": imc,
            "margen_crecimiento": margen_crecimiento,
        }
        ohe = _one_hot_categoricas(
            posicion_principal=e.posicion_principal.value,
            pie_preferido=e.pie_preferido.value,
        )
        filas.append({**base, **ohe})

    df = pd.DataFrame(filas)
    cargar_modelo()
    df = _alinear_columnas(df, _columnas)
    return df


def predecir_batch(entradas: List[JugadorEntrada]) -> List[float]:
    """Predice valores para un lote de jugadores."""
    if not entradas:
        return []
    cargar_modelo()
    X = preparar_features_batch(entradas)
    preds = _modelo.predict(X)
    return [float(v) for v in preds]


def predecir_valor_simple(entrada: EvaluacionSimpleEntrada) -> float:
    """
    Predicción usando solo posición, edad y calificación.

    Asunciones (por defecto, simplificadas):
    - potencial = calificacion_general
    - altura_cm = 180
    - peso_kg = 75
    - pie_preferido: el provisto (default Right)
    """

    e = JugadorEntrada(
        edad=entrada.edad,
        calificacion_general=entrada.calificacion_general,
        potencial=entrada.calificacion_general,
        altura_cm=180,
        peso_kg=75,
        posicion_principal=entrada.posicion_principal,
        pie_preferido=entrada.pie_preferido,
    )
    return predecir_valor(e)


def top_infravalorados(
    top_n: int = 20,
    min_valor_real: int = 500_000,
    anio: Optional[int] = None,
    ascendente: bool = False,
) -> List[JugadorOportunidad]:
    """
    Calcula el Top-N de jugadores infravalorados usando el dataset procesado
    `data/processed/fifa_limpio.csv`.

    - Predice el valor con el modelo y compara contra `valor_euros`.
    - Diferencia positiva = infravalorado (oportunidad).
    - Filtra por `min_valor_real` para ignorar valores muy bajos.
    - Si `anio` se proporciona, filtra por ese año.
    """

    ruta_csv = _data_dir / "fifa_limpio.csv"
    if not ruta_csv.exists():
        raise FileNotFoundError("No se encontró data/processed/fifa_limpio.csv")

    df = pd.read_csv(ruta_csv)
    if anio is not None and "anio" in df.columns:
        df = df[df["anio"] == anio]

    # Construir features de forma vectorizada
    base_cols = [
        "edad",
        "calificacion_general",
        "potencial",
        "altura_cm",
        "peso_kg",
        "imc",
        "margen_crecimiento",
    ]
    faltan = [c for c in base_cols if c not in df.columns]
    if faltan:
        raise ValueError(f"Columnas faltantes en dataset: {faltan}")

    X = df[base_cols].copy()

    # One-hot de posición y pie
    posiciones = [
        "CAM",
        "CB",
        "CDM",
        "CF",
        "CM",
        "GK",
        "LB",
        "LM",
        "LW",
        "LWB",
        "RB",
        "RM",
        "RW",
        "RWB",
        "ST",
    ]
    pies = ["Left", "Right"]

    pos_col = "posicion_principal"
    pie_col = "pie_preferido"
    if pos_col not in df.columns or pie_col not in df.columns:
        raise ValueError("Faltan columnas categóricas requeridas en el dataset")

    for p in posiciones:
        X[f"posicion_principal_{p}"] = (df[pos_col] == p).astype(int)
    for lado in pies:
        X[f"pie_preferido_{lado}"] = (df[pie_col] == lado).astype(int)

    # Alinear columnas y predecir
    cargar_modelo()
    X = _alinear_columnas(X, _columnas)
    y_pred = _modelo.predict(X)

    if "valor_euros" not in df.columns:
        raise ValueError("El dataset no contiene la columna 'valor_euros'")

    df_result = pd.DataFrame(
        {
            "nombre": df.get("nombre_corto", df.get("nombre_completo", "Jugador")),
            "posicion_principal": df[pos_col],
            "edad": df["edad"],
            "calificacion_general": df["calificacion_general"],
            "valor_real": df["valor_euros"].astype(float),
            "valor_predicho": y_pred.astype(float),
        }
    )
    df_result["oportunidad_eur"] = df_result["valor_predicho"] - df_result["valor_real"]
    df_result = df_result[(df_result["oportunidad_eur"] > 0) & (df_result["valor_real"] >= min_valor_real)]
    df_result["oportunidad_pct"] = (df_result["oportunidad_eur"] / df_result["valor_real"]) * 100.0

    df_top = df_result.sort_values("oportunidad_eur", ascending=ascendente).head(top_n)

    # Convertir a esquema de salida
    salidas: List[JugadorOportunidad] = []
    for _, row in df_top.iterrows():
        try:
            pos = row["posicion_principal"]
            pos_enum = pos if isinstance(pos, str) else str(pos)
            salidas.append(
                JugadorOportunidad(
                    nombre=str(row["nombre"]),
                    posicion_principal=pos_enum,  # validación la hace Pydantic Enum
                    edad=int(row["edad"]),
                    calificacion_general=int(row["calificacion_general"]),
                    valor_real=float(row["valor_real"]),
                    valor_predicho=float(row["valor_predicho"]),
                    oportunidad_eur=float(row["oportunidad_eur"]),
                    oportunidad_pct=float(row["oportunidad_pct"]),
                    valor_real_formateado=_fmt_eur_plain(row["valor_real"]),
                    valor_predicho_formateado=_fmt_eur_plain(row["valor_predicho"]),
                    oportunidad_eur_formateado=_fmt_eur_plain(row["oportunidad_eur"]),
                    oportunidad_pct_formateado=f"{float(row['oportunidad_pct']):.1f}%",
                )
            )
        except Exception:
            # Si alguna fila tiene valores fuera del Enum, la omitimos de forma segura
            continue

    return salidas


def top_sobrevalorados(
    top_n: int = 20,
    min_valor_real: int = 500_000,
    anio: Optional[int] = None,
    ascendente: bool = False,
) -> List[JugadorSobreprecio]:
    """
    Calcula el Top-N de jugadores sobrevalorados (sobreprecio) usando el
    dataset procesado `data/processed/fifa_limpio.csv`.
    """

    ruta_csv = _data_dir / "fifa_limpio.csv"
    if not ruta_csv.exists():
        raise FileNotFoundError("No se encontró data/processed/fifa_limpio.csv")

    df = pd.read_csv(ruta_csv)
    if anio is not None and "anio" in df.columns:
        df = df[df["anio"] == anio]

    base_cols = [
        "edad",
        "calificacion_general",
        "potencial",
        "altura_cm",
        "peso_kg",
        "imc",
        "margen_crecimiento",
    ]
    faltan = [c for c in base_cols if c not in df.columns]
    if faltan:
        raise ValueError(f"Columnas faltantes en dataset: {faltan}")

    X = df[base_cols].copy()

    posiciones = [
        "CAM",
        "CB",
        "CDM",
        "CF",
        "CM",
        "GK",
        "LB",
        "LM",
        "LW",
        "LWB",
        "RB",
        "RM",
        "RW",
        "RWB",
        "ST",
    ]
    pies = ["Left", "Right"]

    pos_col = "posicion_principal"
    pie_col = "pie_preferido"
    if pos_col not in df.columns or pie_col not in df.columns:
        raise ValueError("Faltan columnas categóricas requeridas en el dataset")

    for p in posiciones:
        X[f"posicion_principal_{p}"] = (df[pos_col] == p).astype(int)
    for lado in pies:
        X[f"pie_preferido_{lado}"] = (df[pie_col] == lado).astype(int)

    cargar_modelo()
    X = _alinear_columnas(X, _columnas)
    y_pred = _modelo.predict(X)

    if "valor_euros" not in df.columns:
        raise ValueError("El dataset no contiene la columna 'valor_euros'")

    df_result = pd.DataFrame(
        {
            "nombre": df.get("nombre_corto", df.get("nombre_completo", "Jugador")),
            "posicion_principal": df[pos_col],
            "edad": df["edad"],
            "calificacion_general": df["calificacion_general"],
            "valor_real": df["valor_euros"].astype(float),
            "valor_predicho": y_pred.astype(float),
        }
    )
    # sobreprecio = real - predicho > 0
    df_result["sobreprecio_eur"] = df_result["valor_real"] - df_result["valor_predicho"]
    df_result = df_result[(df_result["sobreprecio_eur"] > 0) & (df_result["valor_real"] >= min_valor_real)]
    df_result["sobreprecio_pct"] = (df_result["sobreprecio_eur"] / df_result["valor_real"]) * 100.0

    df_top = df_result.sort_values("sobreprecio_eur", ascending=ascendente).head(top_n)

    salidas: List[JugadorSobreprecio] = []
    for _, row in df_top.iterrows():
        try:
            pos = row["posicion_principal"]
            pos_enum = pos if isinstance(pos, str) else str(pos)
            salidas.append(
                JugadorSobreprecio(
                    nombre=str(row["nombre"]),
                    posicion_principal=pos_enum,
                    edad=int(row["edad"]),
                    calificacion_general=int(row["calificacion_general"]),
                    valor_real=float(row["valor_real"]),
                    valor_predicho=float(row["valor_predicho"]),
                    sobreprecio_eur=float(row["sobreprecio_eur"]),
                    sobreprecio_pct=float(row["sobreprecio_pct"]),
                    valor_real_formateado=_fmt_eur_plain(row["valor_real"]),
                    valor_predicho_formateado=_fmt_eur_plain(row["valor_predicho"]),
                    sobreprecio_eur_formateado=_fmt_eur_plain(row["sobreprecio_eur"]),
                    sobreprecio_pct_formateado=f"{float(row['sobreprecio_pct']):.1f}%",
                )
            )
        except Exception:
            continue

    return salidas
