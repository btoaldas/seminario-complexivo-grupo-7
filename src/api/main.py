from datetime import datetime
from zoneinfo import ZoneInfo

from typing import List, Optional
import time

import os
from fastapi import FastAPI, HTTPException, Request, Response
from src.valoracion import evaluar_valoracion

from .inference import (
    cargar_modelo,
    predecir_valor,
    predecir_batch,
    top_infravalorados,
    top_sobrevalorados,
    _fmt_eur_plain,
)
from .schemas import (
    JugadorEntrada,
    PrediccionValor,
    JugadorEntradaValoracion,
    ValoracionRespuesta,
    ComparacionEntrada,
    ComparacionRespuesta,
    ComparacionItem,
    JugadorOportunidad,
    EvaluacionSimpleEntrada,
    EvaluacionSimpleRespuesta,
    JugadorSobreprecio,
)
from .middlewares import CorrelationIdMiddleware, RateLimiterMiddleware
from .logging_utils import configurar_logging, log_event


app = FastAPI(
    title="API Valoración de Jugadores - Scouting FIFA",
    description=(
        "Servicio de inferencia para estimar el valor de mercado de un jugador.\n\n"
        "El sistema:\n\n"
        "1. Cargará el modelo guardado (modelo_valoracion_fifa.pkl)\n\n"
        "2. Procesará los datos ingresados\n\n"
        "3. Predecirá el valor justo estimado\n\n"
        "4. Si el usuario ingresó el valor actual, lo comparará:\n\n"
        "   - Si valor_real < valor_predicho → INFRAVALORADO 🟢\n\n"
        "   - Si valor_real > valor_predicho → SOBREVALORADO 🔴\n\n"
        "   - Si son similares → BIEN VALORADO 🟡\n\n"
        "Entrenado sobre datos FIFA 15-21."
    ),
    version="1.0.0",
)

configurar_logging()
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RateLimiterMiddleware)


@app.get("/health")
def healthcheck():
    """Ruta de salud para verificar disponibilidad del servicio."""
    try:
        cargar_modelo()
        ok = True
        detalle = "modelo y columnas cargados"
    except Exception as e:
        ok = False
        detalle = f"error: {type(e).__name__}"

    ahora = datetime.now(ZoneInfo("America/Guayaquil")).isoformat()
    return {"ok": ok, "detalle": detalle, "timestamp": ahora}


def _fmt_eur(valor: float | None) -> str | None:
    """Devuelve un string amigable (€, K, M, B) o None si valor es None."""
    if valor is None:
        return None
    v = float(valor)
    sign = "-" if v < 0 else ""
    av = abs(v)
    if av >= 1_000_000_000:
        return f"{sign}€{av/1_000_000_000:.2f}B"
    if av >= 1_000_000:
        return f"{sign}€{av/1_000_000:.2f}M"
    if av >= 1_000:
        return f"{sign}€{av/1_000:.2f}K"
    # miles con separador
    return f"{sign}€{av:,.0f}".replace(",", ".")


@app.post("/predict", response_model=PrediccionValor)
def predict(entrada: JugadorEntrada, request: Request) -> PrediccionValor:
    """
    Predice el valor de mercado estimado en euros.
    """
    inicio = time.perf_counter()
    try:
        valor = predecir_valor(entrada)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se encontró el modelo entrenado. Asegúrate de que exista "
                "'models/modelo_valoracion_fifa.pkl' y 'models/columnas_modelo.pkl'."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {e}")

    dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
    request_id = getattr(request.state, "request_id", None)
    log_event(
        "prediccion_unitaria",
        request_id=request_id,
        dur_ms=dur_ms,
        ruta="/predict",
        status="ok",
    )
    return PrediccionValor(
        id_jugador=entrada.id_jugador,
        valor_estimado=valor,
        moneda="EUR",
        modelo="random_forest",
        valor_estimado_formateado=_fmt_eur(valor),
        nombre_corto=entrada.nombre_corto,
        nombre_completo=entrada.nombre_completo,
    )


@app.post("/evaluate", response_model=ValoracionRespuesta)
def evaluate(entrada: JugadorEntradaValoracion, request: Request) -> ValoracionRespuesta:
    """
    Predice el valor y, si se proporciona `valor_real`, clasifica.

    El sistema:
    1. Cargará el modelo guardado (modelo_valoracion_fifa.pkl)
    2. Procesará los datos ingresados
    3. Predecirá el valor justo estimado
    4. Si el usuario ingresó el valor actual, lo comparará:
       - Si valor_real < valor_predicho → INFRAVALORADO 🟢
       - Si valor_real > valor_predicho → SOBREVALORADO 🔴
       - Si son similares → BIEN VALORADO 🟡
    """

    inicio = time.perf_counter()
    try:
        valor_predicho = predecir_valor(entrada)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se encontró el modelo entrenado. Asegúrate de que exista "
                "'models/modelo_valoracion_fifa.pkl' y 'models/columnas_modelo.pkl'."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {e}")

    resultado = evaluar_valoracion(
        valor_predicho=valor_predicho,
        valor_real=entrada.valor_real,
        tolerancia_relativa=entrada.tolerancia_relativa,
    )

    dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
    request_id = getattr(request.state, "request_id", None)
    log_event(
        "valoracion",
        request_id=request_id,
        dur_ms=dur_ms,
        ruta="/evaluate",
        status="ok",
    )

    return ValoracionRespuesta(
        # id_jugador=entrada.id_jugador,
        valor_predicho=resultado["valor_predicho"],
        valor_real=resultado.get("valor_real"),
        clasificacion=resultado.get("clasificacion"),
        diferencia=resultado.get("diferencia"),
        diferencia_relativa=resultado.get("diferencia_relativa"),
        moneda="EUR",
        valor_predicho_formateado=_fmt_eur(resultado["valor_predicho"]),
        valor_real_formateado=_fmt_eur(resultado.get("valor_real")) if resultado.get("valor_real") is not None else None,
        diferencia_formateada=_fmt_eur(resultado.get("diferencia")) if resultado.get("diferencia") is not None else None,
        nombre_corto=entrada.nombre_corto,
        nombre_completo=entrada.nombre_completo,
    )


@app.post("/predict_batch", response_model=List[PrediccionValor])
def predict_batch(entradas: List[JugadorEntrada], request: Request) -> List[PrediccionValor]:
    """
    Predice valores para múltiples jugadores en una sola llamada.
    """
    inicio = time.perf_counter()
    max_batch = int(os.getenv("MAX_BATCH", "100"))
    if len(entradas) > max_batch:
        raise HTTPException(
            status_code=400,
            detail=f"Lote excede el máximo permitido ({max_batch}).",
        )
    try:
        valores = predecir_batch(entradas)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se encontró el modelo entrenado. Verifique la carpeta models/."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {e}")

    respuestas: List[PrediccionValor] = []
    for e, v in zip(entradas, valores):
        respuestas.append(
            PrediccionValor(
                id_jugador=e.id_jugador,
                valor_estimado=v,
                moneda="EUR",
                modelo="random_forest",
                valor_estimado_formateado=_fmt_eur(v),
                nombre_corto=e.nombre_corto,
                nombre_completo=e.nombre_completo,
            )
        )
    dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
    request_id = getattr(request.state, "request_id", None)
    log_event(
        "prediccion_batch",
        request_id=request_id,
        dur_ms=dur_ms,
        ruta="/predict_batch",
        batch_size=len(entradas),
        status="ok",
    )
    return respuestas


# Comando de ejecución local sugerido:
# uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000


# =============================
# Muestras de solicitudes (para /predict y /evaluate)
# =============================

_SAMPLES_BASE: List[dict] = [
    {
        "id_jugador": "J1",
        "nombre_corto": "L. Messi",
        "nombre_completo": "Lionel Andres Messi",
        "edad": 36,
        "calificacion_general": 91,
        "potencial": 91,
        "altura_cm": 170,
        "peso_kg": 72,
        "posicion_principal": "ST",
        "pie_preferido": "Left",
        "valor_real": 35000000,
    },
    {
        "id_jugador": "J2",
        "nombre_corto": "K. De Bruyne",
        "nombre_completo": "Kevin De Bruyne",
        "edad": 32,
        "calificacion_general": 91,
        "potencial": 91,
        "altura_cm": 181,
        "peso_kg": 70,
        "posicion_principal": "CM",
        "pie_preferido": "Right",
        "valor_real": 80000000,
    },
    {
        "id_jugador": "J3",
        "nombre_corto": "V. van Dijk",
        "nombre_completo": "Virgil van Dijk",
        "edad": 32,
        "calificacion_general": 90,
        "potencial": 90,
        "altura_cm": 193,
        "peso_kg": 92,
        "posicion_principal": "CB",
        "pie_preferido": "Right",
        "valor_real": 70000000,
    },
    {
        "id_jugador": "J4",
        "nombre_corto": "K. Mbappe",
        "nombre_completo": "Kylian Mbappe",
        "edad": 25,
        "calificacion_general": 91,
        "potencial": 95,
        "altura_cm": 178,
        "peso_kg": 75,
        "posicion_principal": "ST",
        "pie_preferido": "Right",
        "valor_real": 180000000,
    },
    {
        "id_jugador": "J5",
        "nombre_corto": "Neymar Jr",
        "nombre_completo": "Neymar da Silva Santos Junior",
        "edad": 32,
        "calificacion_general": 89,
        "potencial": 89,
        "altura_cm": 175,
        "peso_kg": 68,
        "posicion_principal": "LW",
        "pie_preferido": "Right",
        "valor_real": 60000000,
    },
    {
        "id_jugador": "J6",
        "nombre_corto": "L. Modric",
        "nombre_completo": "Luka Modric",
        "edad": 38,
        "calificacion_general": 88,
        "potencial": 88,
        "altura_cm": 172,
        "peso_kg": 66,
        "posicion_principal": "CM",
        "pie_preferido": "Right",
        "valor_real": 10000000,
    },
    {
        "id_jugador": "J7",
        "nombre_corto": "M. Neuer",
        "nombre_completo": "Manuel Neuer",
        "edad": 38,
        "calificacion_general": 87,
        "potencial": 87,
        "altura_cm": 193,
        "peso_kg": 93,
        "posicion_principal": "GK",
        "pie_preferido": "Right",
        "valor_real": 12000000,
    },
    {
        "id_jugador": "J8",
        "nombre_corto": "S. Ramos",
        "nombre_completo": "Sergio Ramos",
        "edad": 38,
        "calificacion_general": 84,
        "potencial": 84,
        "altura_cm": 184,
        "peso_kg": 82,
        "posicion_principal": "CB",
        "pie_preferido": "Right",
        "valor_real": 5000000,
    },
    {
        "id_jugador": "J9",
        "nombre_corto": "N. Kante",
        "nombre_completo": "N'Golo Kante",
        "edad": 33,
        "calificacion_general": 87,
        "potencial": 87,
        "altura_cm": 168,
        "peso_kg": 70,
        "posicion_principal": "CDM",
        "pie_preferido": "Right",
        "valor_real": 20000000,
    },
    {
        "id_jugador": "J10",
        "nombre_corto": "C. Ronaldo",
        "nombre_completo": "Cristiano Ronaldo",
        "edad": 39,
        "calificacion_general": 86,
        "potencial": 86,
        "altura_cm": 187,
        "peso_kg": 83,
        "posicion_principal": "ST",
        "pie_preferido": "Right",
        "valor_real": 15000000,
    },
]


@app.get("/sample_request")
def sample_request(page: int = 1, page_size: int = 5, nombre: Optional[str] = None):
    """
    Devuelve ejemplos listos para copiar/pegar para los endpoints `/predict` y `/evaluate`.

    Soporta paginación mediante `page` y `page_size`.
    """

    if page < 1:
        page = 1
    page_size = max(1, min(50, page_size))
    # aplicar filtro por nombre si viene (en nombre_corto o nombre_completo)
    base = _SAMPLES_BASE
    if nombre:
        q = nombre.strip().lower()
        base = [
            r for r in _SAMPLES_BASE
            if (r.get("nombre_corto") or "").lower().find(q) != -1
            or (r.get("nombre_completo") or "").lower().find(q) != -1
        ]

    total = len(base)
    start = (page - 1) * page_size
    end = start + page_size
    base_slice = base[start:end]

    items = []
    for row in base_slice:
        predict_body = {
            "edad": row["edad"],
            "calificacion_general": row["calificacion_general"],
            "potencial": row["potencial"],
            "altura_cm": row["altura_cm"],
            "peso_kg": row["peso_kg"],
            "posicion_principal": row["posicion_principal"],
            "pie_preferido": row["pie_preferido"],
            "id_jugador": row["id_jugador"],
            "nombre_corto": row["nombre_corto"],
            "nombre_completo": row["nombre_completo"],
        }
        evaluate_body = {**predict_body, "valor_real": row["valor_real"], "tolerancia_relativa": 0.05}
        items.append({"predict": predict_body, "evaluate": evaluate_body})

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items,
        "endpoints": {"predict": "/predict", "evaluate": "/evaluate"},
    }


@app.post("/compare", response_model=ComparacionRespuesta)
def compare(payload: ComparacionEntrada, request: Request) -> ComparacionRespuesta:
    """
    Compara 2–5 jugadores: predicción, diferencia vs `valor_real` (si llega),
    y ranking por "más infravalorado" (gap = valor_predicho - valor_real desc).
    """

    jugadores = payload.jugadores
    if not (2 <= len(jugadores) <= 5):
        raise HTTPException(status_code=400, detail="Debe enviar entre 2 y 5 jugadores")

    inicio = time.perf_counter()
    try:
        # Convertir JugadorEntradaValoracion a JugadorEntrada para predecir_batch
        jugadores_entrada = [
            JugadorEntrada(
                id_jugador=j.id_jugador,
                nombre_corto=j.nombre_corto,
                nombre_completo=j.nombre_completo,
                edad=j.edad,
                calificacion_general=j.calificacion_general,
                potencial=j.potencial,
                altura_cm=j.altura_cm,
                peso_kg=j.peso_kg,
                posicion_principal=j.posicion_principal,
                pie_preferido=j.pie_preferido,
            )
            for j in jugadores
        ]
        preds = predecir_batch(jugadores_entrada)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {e}")

    items: List[ComparacionItem] = []
    for e, vp in zip(jugadores, preds):
        res = evaluar_valoracion(
            valor_predicho=vp,
            valor_real=e.valor_real,
            tolerancia_relativa=e.tolerancia_relativa,
        )
        items.append(
            ComparacionItem(
                id_jugador=e.id_jugador,
                nombre_corto=e.nombre_corto,
                nombre_completo=e.nombre_completo,
                valor_predicho=res["valor_predicho"],
                valor_real=res.get("valor_real"),
                clasificacion=res.get("clasificacion"),
                diferencia=res.get("diferencia"),
                diferencia_relativa=res.get("diferencia_relativa"),
                moneda="EUR",
                valor_predicho_formateado=_fmt_eur(res["valor_predicho"]),
                valor_real_formateado=_fmt_eur(res.get("valor_real")) if res.get("valor_real") is not None else None,
                diferencia_formateada=_fmt_eur(res.get("diferencia")) if res.get("diferencia") is not None else None,
            )
        )

    # Ranking por gap descendente (solo con valor_real presente)
    ranking_items = [it for it in items if it.valor_real is not None and it.diferencia is not None]
    if payload.orden == "pred_desc":
        ranking_items.sort(key=lambda x: x.valor_predicho, reverse=True)
    else:  # gap_desc por defecto
        ranking_items.sort(key=lambda x: x.diferencia or 0, reverse=True)

    dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
    request_id = getattr(request.state, "request_id", None)
    log_event(
        "comparacion",
        request_id=request_id,
        dur_ms=dur_ms,
        ruta="/compare",
        status="ok",
    )

    return ComparacionRespuesta(
        total=len(items),
        orden=payload.orden,
        items=items,
        ranking=ranking_items,
    )


@app.get("/oportunidades_infravaloradas", response_model=List[JugadorOportunidad])
def oportunidades_infravaloradas(
    top_n: int = 20,
    min_valor_real: int = 500_000,
    anio: int | None = None,
    ascendente: bool = False,
    request: Request = None,
):
    """
    Top-N jugadores infravalorados usando el dataset `data/processed/fifa_limpio.csv`.
    - Regresa jugadores con `valor_predicho > valor_real` ordenados por la diferencia.
    - Parámetros: `top_n` (default 20), `min_valor_real` (default €500k), `anio` (opcional).
    """
    try:
        inicio = time.perf_counter()
        resultados = top_infravalorados(
            top_n=top_n, min_valor_real=min_valor_real, anio=anio, ascendente=ascendente
        )
        dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
        request_id = getattr(request.state, "request_id", None) if request else None
        log_event(
            "oportunidades_infravaloradas",
            request_id=request_id,
            dur_ms=dur_ms,
            ruta="/oportunidades_infravaloradas",
            top_n=top_n,
            ascendente=ascendente,
        )
        return resultados
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudo calcular oportunidades: {e}"
        )


@app.get("/top_sobrevalorados", response_model=List[JugadorSobreprecio])
def top_sobrevalorados_endpoint(
    top_n: int = 20,
    min_valor_real: int = 500_000,
    anio: int | None = None,
    ascendente: bool = False,
    request: Request = None,
):
    """
    Top-N jugadores sobrevalorados (sobreprecio = valor_real - valor_predicho > 0).
    """
    try:
        inicio = time.perf_counter()
        resultados = top_sobrevalorados(
            top_n=top_n, min_valor_real=min_valor_real, anio=anio, ascendente=ascendente
        )
        dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
        request_id = getattr(request.state, "request_id", None) if request else None
        log_event(
            "top_sobrevalorados",
            request_id=request_id,
            dur_ms=dur_ms,
            ruta="/top_sobrevalorados",
            top_n=top_n,
            ascendente=ascendente,
        )
        return resultados
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudo calcular sobrevalorados: {e}"
        )


@app.post("/resumen_valor", response_model=EvaluacionSimpleRespuesta)
def resumen_valor(payload: EvaluacionSimpleEntrada, request: Request) -> EvaluacionSimpleRespuesta:
    """
    Endpoint simplificado que acepta solo posición, edad, calificación y valor_real,
    y devuelve un resumen con Valor REAL, Valor PREDICHO y la diferencia como
    OPORTUNIDAD (si predicho > real) o SOBREPRECIO (si real > predicho).
    """
    from .inference import predecir_valor_simple

    inicio = time.perf_counter()
    try:
        valor_predicho = predecir_valor_simple(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {e}")

    real = float(payload.valor_real)
    pred = float(valor_predicho)
    if real >= pred:
        etiqueta = "SOBREPRECIO"
        diferencia = real - pred
    else:
        etiqueta = "OPORTUNIDAD"
        diferencia = pred - real

    porcentaje = (diferencia / real) * 100.0 if real > 0 else 0.0

    dur_ms = round((time.perf_counter() - inicio) * 1000, 2)
    request_id = getattr(request.state, "request_id", None)
    log_event(
        "resumen_valor",
        request_id=request_id,
        dur_ms=dur_ms,
        ruta="/resumen_valor",
        status="ok",
    )

    return EvaluacionSimpleRespuesta(
        posicion_principal=payload.posicion_principal,
        edad=payload.edad,
        calificacion_general=payload.calificacion_general,
        valor_real=real,
        valor_predicho=pred,
        etiqueta=etiqueta,
        diferencia_eur=diferencia,
        porcentaje=round(porcentaje, 1),
        valor_real_formateado=_fmt_eur_plain(real),
        valor_predicho_formateado=_fmt_eur_plain(pred),
        diferencia_formateada=_fmt_eur_plain(diferencia),
        porcentaje_formateado=f"{porcentaje:.1f}%",
    )
