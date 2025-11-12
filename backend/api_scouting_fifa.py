"""
API REST - SISTEMA DE SCOUTING INTELIGENTE FIFA
================================================
Endpoints para búsqueda, filtrado, análisis y predicción de valor de mercado de jugadores.

Basado en:
- Dataset: fifa_limpio.csv (122,501 jugadores × 73 columnas)
- Modelo ML: Random Forest R² = 98.30%
- Artifacts: modelo_fifa.joblib, encoder_fifa.joblib, club_encoding_fifa.joblib

Autor: Sistema Scouting FIFA
Fecha: 8 de noviembre de 2025
"""

import pandas as pd
import numpy as np
import os
import joblib
import unicodedata
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def normalizar_texto(texto):
    """
    Normaliza texto para búsqueda flexible:
    - Convierte a minúsculas
    - Elimina tildes y acentos
    - Útil para búsqueda insensible a mayúsculas y acentos
    """
    if pd.isna(texto) or texto is None:
        return ""
    texto = str(texto).lower()
    # Eliminar tildes usando unicodedata
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto


# ============================================================================
# CONFIGURACIÓN DE RUTAS Y CARGA DE ARCHIVOS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "datos", "modelos")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_fifa.joblib")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder_fifa.joblib")
CLUB_ENCODING_PATH = os.path.join(MODEL_DIR, "club_encoding_fifa.joblib")

# Cargar modelo y archivos
print("Cargando modelo y datos...")
print(f"  - Cargando modelo desde: {MODEL_PATH}")
modelo = joblib.load(MODEL_PATH)
print(f"  ✓ Modelo cargado")

print(f"  - Cargando encoder desde: {ENCODER_PATH}")
encoder = joblib.load(ENCODER_PATH)
print(f"  ✓ Encoder cargado")

print(f"  - Cargando club encoding desde: {CLUB_ENCODING_PATH}")
club_encoding = joblib.load(CLUB_ENCODING_PATH)
print(f"  ✓ Club encoding cargado")

print(f"  - Cargando dataset desde Parquet (7x más rápido)...")
PARQUET_PATH = DATA_PATH.replace('.csv', '.parquet')
try:
    df_jugadores = pd.read_parquet(PARQUET_PATH)
    print(f"  ✓ Dataset Parquet cargado: {len(df_jugadores):,} jugadores")
except FileNotFoundError:
    print(f"  ⚠️  Parquet no encontrado, cargando CSV...")
    df_jugadores = pd.read_csv(DATA_PATH, low_memory=False)
    print(f"  ✓ Dataset CSV cargado: {len(df_jugadores):,} jugadores")

print("\n✓ TODOS LOS COMPONENTES CARGADOS EXITOSAMENTE")

# Inicializar FastAPI
app = FastAPI(
    title="API Sistema Scouting Inteligente FIFA",
    description="API REST para búsqueda, análisis y predicción de valor de mercado de jugadores de fútbol",
    version="2.0.0"
)


# ============================================================================
# MODELOS PYDANTIC PARA VALIDACIÓN DE DATOS
# ============================================================================

class DatosJugadorPrediccion(BaseModel):
    """
    Modelo para recibir datos de un jugador y predecir su valor de mercado.
    Todos los campos son opcionales para permitir predicciones parciales.
    """
    # Información básica
    edad: Optional[int] = Field(None, ge=16, le=45, description="Edad del jugador (16-45 años)")
    
    # Atributos técnicos principales (0-100)
    valoracion_global: Optional[int] = Field(None, ge=40, le=100, description="Valoración global FIFA (40-100)")
    potencial: Optional[int] = Field(None, ge=40, le=100, description="Potencial del jugador (40-100)")
    ritmo_velocidad: Optional[int] = Field(None, ge=0, le=100, description="Atributo de ritmo/velocidad")
    tiro_disparo: Optional[int] = Field(None, ge=0, le=100, description="Atributo de tiro")
    pase: Optional[int] = Field(None, ge=0, le=100, description="Atributo de pase")
    regate_gambeta: Optional[int] = Field(None, ge=0, le=100, description="Atributo de regate")
    defensa: Optional[int] = Field(None, ge=0, le=100, description="Atributo de defensa")
    fisico: Optional[int] = Field(None, ge=0, le=100, description="Atributo físico")
    
    # Información adicional
    pie_debil: Optional[int] = Field(None, ge=1, le=5, description="Habilidad pie débil (1-5)")
    habilidades_regate: Optional[int] = Field(None, ge=1, le=5, description="Habilidad de regate (1-5)")
    reputacion_internacional: Optional[int] = Field(None, ge=1, le=5, description="Reputación internacional (1-5)")
    
    # Información categórica
    club: Optional[str] = Field(None, description="Club actual del jugador")
    liga: Optional[str] = Field(None, description="Liga donde juega")
    posiciones_jugador: Optional[str] = Field(None, description="Posición del jugador (ej: ST, CM, CB)")
    nacionalidad: Optional[str] = Field(None, description="Nacionalidad del jugador")
    pie_preferido: Optional[str] = Field(None, description="Pie preferido (Left o Right)")
    ritmo_trabajo: Optional[str] = Field(None, description="Ritmo de trabajo (ej: High/Medium)")
    
    # Features calculadas opcionales
    altura_cm: Optional[float] = Field(None, ge=150, le=210, description="Altura en cm")
    peso_kg: Optional[float] = Field(None, ge=50, le=110, description="Peso en kg")
    
    class Config:
        json_schema_extra = {
            "example": {
                "edad": 25,
                "valoracion_global": 85,
                "potencial": 88,
                "ritmo_velocidad": 85,
                "tiro_disparo": 80,
                "pase": 75,
                "regate_gambeta": 82,
                "defensa": 35,
                "fisico": 70,
                "pie_debil": 4,
                "habilidades_regate": 4,
                "reputacion_internacional": 3,
                "club": "FC Barcelona",
                "liga": "Spain Primera Division",
                "posiciones_jugador": "LW, ST",
                "nacionalidad": "Brazil",
                "pie_preferido": "Right",
                "ritmo_trabajo": "High/Medium",
                "altura_cm": 175,
                "peso_kg": 68
            }
        }


class RespuestaPrediccion(BaseModel):
    """Respuesta del endpoint de predicción"""
    valor_predicho_eur: float = Field(..., description="Valor de mercado predicho en EUR")
    valor_predicho_formateado: str = Field(..., description="Valor formateado (ej: €5.2M)")
    confianza_prediccion: str = Field(..., description="Nivel de confianza (Alta/Media/Baja)")
    percentil_valor: int = Field(..., description="Percentil del valor predicho (0-100)")
    categoria_valor: str = Field(..., description="Categoría del valor (Bajo/Medio/Alto/Muy Alto)")
    features_utilizadas: int = Field(..., description="Cantidad de features proporcionadas")
    features_imputadas: int = Field(..., description="Cantidad de features imputadas")


# ============================================================================
# ENDPOINT 1: OBTENER OPCIONES DE FILTROS
# ============================================================================

@app.get(
    "/jugadores/filtros",
    summary="Obtener opciones de filtros",
    description="Devuelve todas las opciones únicas disponibles para los filtros del dashboard"
)
def obtener_opciones_filtros():
    """
    Endpoint que retorna listas de valores únicos para todos los filtros.
    Útil para poblar dropdowns y selectboxes en el frontend.
    """
    try:
        return {
            "posiciones": sorted(df_jugadores["posiciones_jugador"].dropna().unique().tolist()),
            "nacionalidades": sorted(df_jugadores["nacionalidad"].dropna().unique().tolist()),
            "clubes": sorted(df_jugadores["club"].dropna().unique().tolist()),
            "ligas": sorted(df_jugadores["liga"].dropna().unique().tolist()),
            "categorias_edad": sorted(df_jugadores["categoria_edad"].dropna().unique().tolist()),
            "categorias_posicion": sorted(df_jugadores["categoria_posicion"].dropna().unique().tolist()),
            "categorias_reputacion": sorted(df_jugadores["categoria_reputacion"].dropna().unique().tolist()),
            "pies_preferidos": sorted(df_jugadores["pie_preferido"].dropna().unique().tolist()),
            "rangos": {
                "edad_min": int(df_jugadores["edad"].min()),
                "edad_max": int(df_jugadores["edad"].max()),
                "valoracion_min": int(df_jugadores["valoracion_global"].min()),
                "valoracion_max": int(df_jugadores["valoracion_global"].max()),
                "potencial_min": int(df_jugadores["potencial"].min()),
                "potencial_max": int(df_jugadores["potencial"].max()),
                "valor_min_eur": float(df_jugadores["valor_mercado_eur"].min()),
                "valor_max_eur": float(df_jugadores["valor_mercado_eur"].max())
            },
            "total_jugadores": len(df_jugadores)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener filtros: {str(e)}")


# ============================================================================
# ENDPOINT 2: BUSCAR JUGADORES CON FILTROS
# ============================================================================

@app.get(
    "/jugadores/buscar",
    summary="Buscar jugadores con filtros",
    description="Busca jugadores aplicando múltiples filtros personalizables con búsqueda flexible por nombre"
)
def buscar_jugadores(
    nombre: Optional[str] = Query(None, description="Buscar por nombre (parcial, sin tildes, case-insensitive)"),
    posicion: Optional[List[str]] = Query(None, description="Filtrar por posiciones (ej: ST, CM)"),
    nacionalidad: Optional[List[str]] = Query(None, description="Filtrar por nacionalidades"),
    club: Optional[List[str]] = Query(None, description="Filtrar por clubes"),
    liga: Optional[List[str]] = Query(None, description="Filtrar por ligas"),
    edad_min: Optional[int] = Query(None, ge=16, le=45, description="Edad mínima"),
    edad_max: Optional[int] = Query(None, ge=16, le=45, description="Edad máxima"),
    valoracion_min: Optional[int] = Query(None, ge=40, le=100, description="Valoración global mínima"),
    valoracion_max: Optional[int] = Query(None, ge=40, le=100, description="Valoración global máxima"),
    potencial_min: Optional[int] = Query(None, ge=40, le=100, description="Potencial mínimo"),
    potencial_max: Optional[int] = Query(None, ge=40, le=100, description="Potencial máximo"),
    valor_min_eur: Optional[float] = Query(None, description="Valor mínimo de mercado en EUR"),
    valor_max_eur: Optional[float] = Query(None, description="Valor máximo de mercado en EUR"),
    año_datos: Optional[int] = Query(None, ge=2015, le=2021, description="Año FIFA (2015-2021)"),
    categoria_edad: Optional[List[str]] = Query(None, description="Categoría de edad (Joven/Prime/Veterano)"),
    categoria_posicion: Optional[List[str]] = Query(None, description="Categoría de posición"),
    pie_preferido: Optional[str] = Query(None, description="Pie preferido (Left/Right)"),
    clasificacion_ml: Optional[List[str]] = Query(None, description="Clasificación ML (INFRAVALORADO/SOBREVALORADO/JUSTO)"),
    limite: Optional[int] = Query(100, ge=1, le=1000, description="Límite de resultados"),
    ordenar_por: Optional[str] = Query("valor_mercado_eur", description="Campo para ordenar"),
    orden_descendente: Optional[bool] = Query(True, description="Orden descendente")
):
    """
    Busca jugadores aplicando filtros combinados.
    Búsqueda flexible por nombre: parcial, sin tildes, mayúsculas/minúsculas.
    Retorna lista de jugadores con información resumida.
    """
    try:
        df_filtrado = df_jugadores.copy()
        
        # ⚽ FILTRO POR NOMBRE (BÚSQUEDA FLEXIBLE)
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            # Crear columnas temporales normalizadas para búsqueda eficiente
            df_filtrado['nombre_completo_normalizado'] = df_filtrado['nombre_completo'].apply(normalizar_texto)
            df_filtrado['nombre_corto_normalizado'] = df_filtrado['nombre_corto'].apply(normalizar_texto)
            
            # Buscar en nombre completo O nombre corto (búsqueda parcial)
            mascara_nombre = (
                df_filtrado['nombre_completo_normalizado'].str.contains(nombre_normalizado, na=False) |
                df_filtrado['nombre_corto_normalizado'].str.contains(nombre_normalizado, na=False)
            )
            df_filtrado = df_filtrado[mascara_nombre]
            
            # Eliminar columnas temporales
            df_filtrado = df_filtrado.drop(['nombre_completo_normalizado', 'nombre_corto_normalizado'], axis=1)
        
        # Aplicar filtros
        if posicion:
            df_filtrado = df_filtrado[df_filtrado["posiciones_jugador"].isin(posicion)]
        
        if nacionalidad:
            df_filtrado = df_filtrado[df_filtrado["nacionalidad"].isin(nacionalidad)]
        
        if club:
            df_filtrado = df_filtrado[df_filtrado["club"].isin(club)]
        
        if liga:
            df_filtrado = df_filtrado[df_filtrado["liga"].isin(liga)]
        
        if edad_min is not None:
            df_filtrado = df_filtrado[df_filtrado["edad"] >= edad_min]
        
        if edad_max is not None:
            df_filtrado = df_filtrado[df_filtrado["edad"] <= edad_max]
        
        if valoracion_min is not None:
            df_filtrado = df_filtrado[df_filtrado["valoracion_global"] >= valoracion_min]
        
        if valoracion_max is not None:
            df_filtrado = df_filtrado[df_filtrado["valoracion_global"] <= valoracion_max]
        
        if potencial_min is not None:
            df_filtrado = df_filtrado[df_filtrado["potencial"] >= potencial_min]
        
        if potencial_max is not None:
            df_filtrado = df_filtrado[df_filtrado["potencial"] <= potencial_max]
        
        if valor_min_eur is not None:
            df_filtrado = df_filtrado[df_filtrado["valor_mercado_eur"] >= valor_min_eur]
        
        if valor_max_eur is not None:
            df_filtrado = df_filtrado[df_filtrado["valor_mercado_eur"] <= valor_max_eur]
        
        # ⚽ FILTRO DE AÑO FIFA (NUEVO)
        if año_datos is not None:
            if "año_datos" in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado["año_datos"] == año_datos]
        
        if categoria_edad:
            df_filtrado = df_filtrado[df_filtrado["categoria_edad"].isin(categoria_edad)]
        
        if categoria_posicion:
            df_filtrado = df_filtrado[df_filtrado["categoria_posicion"].isin(categoria_posicion)]
        
        if pie_preferido:
            df_filtrado = df_filtrado[df_filtrado["pie_preferido"] == pie_preferido]
        
        # 💎 FILTRO DE CLASIFICACIÓN ML (NUEVO)
        if clasificacion_ml:
            if "clasificacion_ml" in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado["clasificacion_ml"].isin(clasificacion_ml)]
        
        # Ordenar resultados
        if ordenar_por in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by=ordenar_por, ascending=not orden_descendente)
        
        # Limitar resultados
        df_filtrado = df_filtrado.head(limite)
        
        # Seleccionar columnas para respuesta
        columnas_respuesta = [
            "id_sofifa", "nombre_corto", "edad", "nacionalidad", "club", "liga",
            "posiciones_jugador", "valoracion_global", "potencial", "valor_mercado_eur",
            "salario_eur", "pie_preferido", "altura_cm", "peso_kg", "url_jugador"
        ]
        
        # Agregar año_datos si existe en el DataFrame
        if "año_datos" in df_filtrado.columns:
            columnas_respuesta.append("año_datos")
        
        # Agregar clasificacion_ml si existe en el DataFrame
        if "clasificacion_ml" in df_filtrado.columns:
            columnas_respuesta.append("clasificacion_ml")
        
        jugadores_encontrados = df_filtrado[columnas_respuesta].to_dict("records")
        
        return {
            "total_encontrados": len(df_filtrado),
            "total_dataset": len(df_jugadores),
            "jugadores": jugadores_encontrados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda: {str(e)}")


# ============================================================================
# ENDPOINT 3: PERFIL COMPLETO DE UN JUGADOR
# ============================================================================

@app.get(
    "/jugadores/{jugador_id}/perfil",
    summary="Obtener perfil completo de un jugador",
    description="Retorna todos los atributos de un jugador específico más su valor predicho"
)
def obtener_perfil_jugador(jugador_id: int, año: int = Query(None, description="Año FIFA específico del jugador")):
    """
    Obtiene el perfil completo de un jugador por su ID de SoFIFA.
    Incluye todos sus atributos y el valor predicho por el modelo ML.
    Si se proporciona el parámetro año, devuelve el perfil de ese año específico.
    """
    try:
        # Filtrar por ID y año si se proporciona
        if año:
            jugador = df_jugadores[(df_jugadores["id_sofifa"] == jugador_id) & (df_jugadores["año_datos"] == año)]
        else:
            jugador = df_jugadores[df_jugadores["id_sofifa"] == jugador_id]
        
        if jugador.empty:
            raise HTTPException(status_code=404, detail=f"Jugador con ID {jugador_id}{f' en el año {año}' if año else ''} no encontrado")
        
        jugador_dict = jugador.iloc[0].to_dict()
        
        # Preparar datos para predicción
        datos_prediccion = preparar_datos_para_prediccion(jugador.iloc[0])
        
        try:
            valor_predicho = modelo.predict(datos_prediccion)[0]
            valor_predicho_eur = np.expm1(valor_predicho)  # Revertir log1p
            
            valor_real = jugador_dict["valor_mercado_eur"]
            # LÓGICA CORRECTA: valor_real - valor_predicho
            diferencia = valor_real - valor_predicho_eur
            diferencia_porcentual = (diferencia / valor_predicho_eur * 100) if valor_predicho_eur > 0 else 0
            
            # Clasificar jugador
            # Si diferencia NEGATIVA (valor_real < valor_predicho) → INFRAVALORADO
            if diferencia_porcentual < -20:
                clasificacion = "Infravalorado"
            # Si diferencia POSITIVA (valor_real > valor_predicho) → SOBREVALORADO
            elif diferencia_porcentual > 20:
                clasificacion = "Sobrevalorado"
            else:
                clasificacion = "Valor Justo"
            
            prediccion_info = {
                "valor_predicho_eur": float(valor_predicho_eur),
                "valor_real_eur": float(valor_real),
                "diferencia_eur": float(diferencia),
                "diferencia_porcentual": float(diferencia_porcentual),
                "clasificacion": clasificacion
            }
        except Exception as e:
            prediccion_info = {"error_prediccion": str(e)}
        
        return {
            "jugador": jugador_dict,
            "prediccion_ml": prediccion_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener perfil: {str(e)}")


@app.get("/jugadores/{jugador_id}/años", tags=["Jugadores"])
def obtener_años_jugador(jugador_id: int):
    """
    Obtiene todos los años FIFA en los que un jugador específico está presente en la base de datos.
    """
    try:
        # Filtrar todos los registros del jugador por su id_sofifa
        registros_jugador = df_jugadores[df_jugadores["id_sofifa"] == jugador_id]
        
        if registros_jugador.empty:
            raise HTTPException(status_code=404, detail=f"Jugador con ID {jugador_id} no encontrado")
        
        # Obtener años únicos ordenados
        años_disponibles = sorted(registros_jugador["año_datos"].unique().tolist(), reverse=True)
        
        return {
            "id_sofifa": jugador_id,
            "años": años_disponibles,
            "total_registros": len(años_disponibles)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener años del jugador: {str(e)}")


# ============================================================================
# ENDPOINT 4: PREDECIR VALOR DE MERCADO (ML)
# ============================================================================

@app.post(
    "/ml/predecir_valor",
    summary="Predecir valor de mercado de un jugador",
    description="Recibe atributos de un jugador y predice su valor de mercado usando el modelo ML",
    response_model=RespuestaPrediccion
)
def predecir_valor_jugador(datos: DatosJugadorPrediccion):
    """
    Endpoint principal de Machine Learning.
    Recibe atributos parciales o completos de un jugador y predice su valor de mercado.
    
    El modelo puede trabajar con datos incompletos, imputando valores faltantes.
    """
    try:
        # Convertir datos de entrada a diccionario
        datos_dict = datos.model_dump(exclude_none=True)
        features_proporcionadas = len(datos_dict)
        
        # Crear DataFrame con los datos proporcionados
        df_input = pd.DataFrame([datos_dict])
        
        # Imputar valores faltantes con medianas/modas del dataset
        df_input = imputar_valores_faltantes(df_input)
        
        # Preparar datos para el modelo (mismo preprocesamiento que entrenamiento)
        X_prediccion = preparar_datos_para_prediccion_api(df_input)
        
        features_totales = X_prediccion.shape[1]
        features_imputadas = features_totales - features_proporcionadas
        
        # Realizar predicción
        valor_log = modelo.predict(X_prediccion)[0]
        valor_eur = np.expm1(valor_log)  # Revertir transformación log1p
        
        # Calcular confianza basada en features proporcionadas
        porcentaje_features = (features_proporcionadas / 20) * 100  # 20 features clave aprox
        if porcentaje_features >= 80:
            confianza = "Alta"
        elif porcentaje_features >= 50:
            confianza = "Media"
        else:
            confianza = "Baja"
        
        # Calcular percentil del valor predicho
        valores_dataset = df_jugadores["valor_mercado_eur"].values
        percentil = int((valores_dataset < valor_eur).sum() / len(valores_dataset) * 100)
        
        # Categorizar valor
        if valor_eur >= 50_000_000:
            categoria = "Muy Alto (Top 1%)"
        elif valor_eur >= 10_000_000:
            categoria = "Alto (Top 10%)"
        elif valor_eur >= 1_000_000:
            categoria = "Medio (Top 50%)"
        else:
            categoria = "Bajo"
        
        # Formatear valor
        if valor_eur >= 1_000_000:
            valor_formateado = f"€{valor_eur/1_000_000:.2f}M"
        else:
            valor_formateado = f"€{valor_eur:,.0f}"
        
        return RespuestaPrediccion(
            valor_predicho_eur=float(valor_eur),
            valor_predicho_formateado=valor_formateado,
            confianza_prediccion=confianza,
            percentil_valor=percentil,
            categoria_valor=categoria,
            features_utilizadas=features_proporcionadas,
            features_imputadas=features_imputadas
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")


# ============================================================================
# ENDPOINT 5: TOP JUGADORES INFRAVALORADOS
# ============================================================================

@app.get(
    "/jugadores/infravalorados",
    summary="Top jugadores infravalorados",
    description="Retorna jugadores cuyo valor predicho supera significativamente su valor de mercado actual"
)
def obtener_jugadores_infravalorados(
    top: int = Query(10, ge=1, le=100, description="Cantidad de jugadores a retornar"),
    diferencia_minima_porcentual: float = Query(10.0, description="Diferencia mínima % para considerar infravalorado"),
    edad_maxima: Optional[int] = Query(None, description="Edad máxima para filtrar"),
    posicion: Optional[List[str]] = Query(None, description="Filtrar por posiciones")
):
    """
    Identifica oportunidades de mercado: jugadores infravalorados.
    
    Criterio: valor_predicho > valor_actual + diferencia_minima%
    """
    try:
        # Hacer predicciones para todo el dataset (o usar caché si existe)
        df_con_predicciones = calcular_predicciones_dataset()
        
        # Filtrar por edad si se especifica
        if edad_maxima:
            df_con_predicciones = df_con_predicciones[df_con_predicciones["edad"] <= edad_maxima]
        
        # Filtrar por posición si se especifica
        if posicion:
            df_con_predicciones = df_con_predicciones[
                df_con_predicciones["posiciones_jugador"].isin(posicion)
            ]
        
        # Filtrar jugadores con valor de mercado > 0 para evitar división por cero
        df_con_predicciones = df_con_predicciones[df_con_predicciones["valor_mercado_eur"] > 0]
        
        # Calcular diferencia porcentual
        df_con_predicciones["diferencia_porcentual"] = (
            (df_con_predicciones["valor_predicho_eur"] - df_con_predicciones["valor_mercado_eur"]) 
            / df_con_predicciones["valor_mercado_eur"] * 100
        )
        
        # Reemplazar valores infinitos o NaN con 0
        df_con_predicciones["diferencia_porcentual"] = df_con_predicciones["diferencia_porcentual"].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        # Filtrar infravalorados
        df_infravalorados = df_con_predicciones[
            df_con_predicciones["diferencia_porcentual"] >= diferencia_minima_porcentual
        ]
        
        # Ordenar por diferencia porcentual descendente
        df_infravalorados = df_infravalorados.sort_values("diferencia_porcentual", ascending=False)
        
        # Tomar top N
        df_top = df_infravalorados.head(top)
        
        # Seleccionar columnas relevantes
        columnas_resultado = [
            "id_sofifa", "nombre_corto", "edad", "nacionalidad", "club", "liga",
            "posiciones_jugador", "valoracion_global", "potencial",
            "valor_mercado_eur", "valor_predicho_eur", "diferencia_porcentual", "url_jugador"
        ]
        
        resultados = df_top[columnas_resultado].to_dict("records")
        
        return {
            "total_infravalorados": len(df_infravalorados),
            "top_jugadores": resultados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular infravalorados: {str(e)}")


# ============================================================================
# ENDPOINT 6: TOP JUGADORES SOBREVALORADOS
# ============================================================================

@app.get(
    "/jugadores/sobrevalorados",
    summary="Top jugadores sobrevalorados",
    description="Retorna jugadores cuyo valor de mercado actual supera significativamente su valor predicho"
)
def obtener_jugadores_sobrevalorados(
    top: int = Query(10, ge=1, le=100, description="Cantidad de jugadores a retornar"),
    diferencia_minima_porcentual: float = Query(10.0, description="Diferencia mínima % para considerar sobrevalorado")
):
    """
    Identifica jugadores potencialmente sobrevalorados en el mercado.
    
    Criterio: valor_actual > valor_predicho + diferencia_minima%
    """
    try:
        df_con_predicciones = calcular_predicciones_dataset()
        
        # Filtrar jugadores con valor de mercado > 0 para evitar división por cero
        df_con_predicciones = df_con_predicciones[df_con_predicciones["valor_mercado_eur"] > 0]
        
        # Calcular diferencia porcentual (negativa para sobrevalorados)
        df_con_predicciones["diferencia_porcentual"] = (
            (df_con_predicciones["valor_predicho_eur"] - df_con_predicciones["valor_mercado_eur"]) 
            / df_con_predicciones["valor_mercado_eur"] * 100
        )
        
        # Reemplazar valores infinitos o NaN con 0
        df_con_predicciones["diferencia_porcentual"] = df_con_predicciones["diferencia_porcentual"].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        # Filtrar sobrevalorados (diferencia negativa)
        df_sobrevalorados = df_con_predicciones[
            df_con_predicciones["diferencia_porcentual"] <= -diferencia_minima_porcentual
        ]
        
        # Ordenar por diferencia porcentual ascendente (más negativo = más sobrevalorado)
        df_sobrevalorados = df_sobrevalorados.sort_values("diferencia_porcentual", ascending=True)
        
        # Tomar top N
        df_top = df_sobrevalorados.head(top)
        
        columnas_resultado = [
            "id_sofifa", "nombre_corto", "edad", "nacionalidad", "club", "liga",
            "posiciones_jugador", "valoracion_global", "potencial",
            "valor_mercado_eur", "valor_predicho_eur", "diferencia_porcentual", "url_jugador"
        ]
        
        resultados = df_top[columnas_resultado].to_dict("records")
        
        return {
            "total_sobrevalorados": len(df_sobrevalorados),
            "top_jugadores": resultados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular sobrevalorados: {str(e)}")


# ============================================================================
# ENDPOINT 7: ESTADÍSTICAS GENERALES DEL DATASET
# ============================================================================

@app.get(
    "/eda/estadisticas_generales",
    summary="Estadísticas generales del dataset",
    description="Retorna KPIs generales del dataset de jugadores"
)
def obtener_estadisticas_generales():
    """
    Endpoint para obtener estadísticas generales y KPIs del dataset.
    Útil para el dashboard principal.
    """
    try:
        return {
            "total_jugadores": int(len(df_jugadores)),
            "total_clubes": int(df_jugadores["club"].nunique()),
            "total_ligas": int(df_jugadores["liga"].nunique()),
            "total_nacionalidades": int(df_jugadores["nacionalidad"].nunique()),
            "edad_promedio": float(df_jugadores["edad"].mean()),
            "valoracion_promedio": float(df_jugadores["valoracion_global"].mean()),
            "valor_mercado_promedio_eur": float(df_jugadores["valor_mercado_eur"].mean()),
            "valor_mercado_total_eur": float(df_jugadores["valor_mercado_eur"].sum()),
            "valor_mercado_mediana_eur": float(df_jugadores["valor_mercado_eur"].median()),
            "jugador_mas_valioso": {
                "nombre": df_jugadores.loc[df_jugadores["valor_mercado_eur"].idxmax(), "nombre_corto"],
                "valor_eur": float(df_jugadores["valor_mercado_eur"].max()),
                "club": df_jugadores.loc[df_jugadores["valor_mercado_eur"].idxmax(), "club"]
            },
            "club_mas_valioso": {
                "nombre": df_jugadores.groupby("club")["valor_mercado_eur"].sum().idxmax(),
                "valor_total_eur": float(df_jugadores.groupby("club")["valor_mercado_eur"].sum().max())
            },
            "liga_mas_valiosa": {
                "nombre": df_jugadores.groupby("liga")["valor_mercado_eur"].sum().idxmax(),
                "valor_total_eur": float(df_jugadores.groupby("liga")["valor_mercado_eur"].sum().max())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular estadísticas: {str(e)}")


@app.get(
    "/eda/jugador_mas_valioso",
    summary="Obtener jugador más valioso",
    description="Retorna el jugador más valioso del dataset, opcionalmente filtrado por año"
)
def obtener_jugador_mas_valioso(año: int = Query(None, description="Año FIFA específico (opcional)")):
    """
    Obtiene el jugador más valioso del dataset.
    Si se proporciona el parámetro año, filtra por ese año específico.
    """
    try:
        # Filtrar por año si se proporciona
        if año:
            df_filtrado = df_jugadores[df_jugadores["año_datos"] == año]
            if df_filtrado.empty:
                raise HTTPException(status_code=404, detail=f"No hay datos para el año {año}")
        else:
            df_filtrado = df_jugadores
        
        # Obtener el jugador más valioso
        idx_max = df_filtrado["valor_mercado_eur"].idxmax()
        jugador = df_filtrado.loc[idx_max]
        
        return {
            "id_sofifa": int(jugador["id_sofifa"]),
            "nombre": jugador["nombre_corto"],
            "nombre_completo": jugador.get("nombre_largo", jugador["nombre_corto"]),
            "valor_eur": float(jugador["valor_mercado_eur"]),
            "club": jugador["club"],
            "liga": jugador["liga"],
            "nacionalidad": jugador["nacionalidad"],
            "edad": int(jugador["edad"]),
            "posicion": jugador["posiciones_jugador"],
            "valoracion": int(jugador["valoracion_global"]),
            "potencial": int(jugador["potencial"]),
            "año_datos": int(jugador["año_datos"])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener jugador más valioso: {str(e)}")


# ============================================================================
# ENDPOINT 8: DATOS PARA GRÁFICOS DEL DASHBOARD
# ============================================================================

@app.get(
    "/eda/datos_graficos",
    summary="Obtener datos para gráficos",
    description="Retorna datos agregados para visualizaciones del dashboard"
)
def obtener_datos_graficos(
    tipo_analisis: str = Query(..., description="Tipo de análisis: posiciones, nacionalidades, clubes, ligas, edades"),
    top_n: int = Query(20, ge=5, le=50, description="Cantidad de elementos a retornar")
):
    """
    Endpoint para obtener datos agregados para diferentes tipos de gráficos.
    """
    try:
        if tipo_analisis == "posiciones":
            # Distribución por posiciones
            datos = df_jugadores["categoria_posicion"].value_counts().head(top_n).reset_index()
            datos.columns = ["categoria", "cantidad"]
            
        elif tipo_analisis == "nacionalidades":
            # Top nacionalidades por valor promedio
            datos = df_jugadores.groupby("nacionalidad").agg({
                "valor_mercado_eur": "mean",
                "id_sofifa": "count"
            }).sort_values("valor_mercado_eur", ascending=False).head(top_n).reset_index()
            datos.columns = ["nacionalidad", "valor_promedio_eur", "cantidad_jugadores"]
            
        elif tipo_analisis == "clubes":
            # Top clubes por valor total de plantilla
            datos = df_jugadores.groupby("club").agg({
                "valor_mercado_eur": ["sum", "mean", "count"]
            }).sort_values(("valor_mercado_eur", "sum"), ascending=False).head(top_n).reset_index()
            datos.columns = ["club", "valor_total_eur", "valor_promedio_eur", "cantidad_jugadores"]
            
        elif tipo_analisis == "ligas":
            # Top ligas por valor promedio
            datos = df_jugadores.groupby("liga").agg({
                "valor_mercado_eur": ["sum", "mean", "count"]
            }).sort_values(("valor_mercado_eur", "mean"), ascending=False).head(top_n).reset_index()
            datos.columns = ["liga", "valor_total_eur", "valor_promedio_eur", "cantidad_jugadores"]
            
        elif tipo_analisis == "edades":
            # Distribución por categorías de edad
            datos = df_jugadores.groupby("categoria_edad").agg({
                "valor_mercado_eur": "mean",
                "id_sofifa": "count"
            }).reset_index()
            datos.columns = ["categoria_edad", "valor_promedio_eur", "cantidad_jugadores"]
            
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de análisis '{tipo_analisis}' no soportado")
        
        return {
            "tipo_analisis": tipo_analisis,
            "datos": datos.to_dict("records")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar datos gráficos: {str(e)}")


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def preparar_datos_para_prediccion(jugador_serie):
    """
    Prepara los datos de un jugador (Serie de pandas) para hacer predicción.
    Replica el preprocesamiento del entrenamiento.
    """
    # Crear DataFrame de una fila
    df = pd.DataFrame([jugador_serie])
    
    # Aplicar mismo preprocesamiento que en entrenamiento
    return preparar_datos_para_prediccion_api(df)


def preparar_datos_para_prediccion_api(df_input):
    """
    Prepara datos de entrada de la API para predicción ML.
    Replica EXACTAMENTE el preprocesamiento de entrenamiento.py
    """
    # IMPORTANTE: Estas columnas deben coincidir EXACTAMENTE con preprocesamiento_modelo.py
    
    # Columnas numéricas (ORDEN EXACTO del entrenamiento)
    col_numericas = [
        # TOP FEATURES
        "reputacion_internacional",
        "valoracion_global",
        "potencial",
        "movimiento_reacciones",
        # FEATURES MODERADAS
        "calidad_promedio",
        "pase",
        "mentalidad_compostura",
        "regate_gambeta",
        "mentalidad_vision",
        "tiro_disparo",
        "ataque_pase_corto",
        # FEATURES ADICIONALES
        "ataque_definicion",
        "ataque_cabezazo",
        "ataque_centros",
        "ataque_voleas",
        # Atributos físicos
        "movimiento_velocidad_sprint",
        "movimiento_aceleracion",
        "movimiento_agilidad",
        "movimiento_equilibrio",
        "fisico",
        # Atributos defensivos
        "defensa",
        "defensa_entrada_pie",
        "defensa_entrada_deslizante",
        "defensa_marcaje",
        # Atributos mentales
        "mentalidad_agresividad",
        "mentalidad_intercepciones",
        "mentalidad_posicionamiento",
        "mentalidad_penales",
        # Habilidades
        "pie_debil",
        "habilidades_regate",
        "habilidad_regate",
        "habilidad_control_balon",
        "habilidad_efecto",
        "habilidad_pase_largo",
        "habilidad_tiros_libres",
        # Features calculadas
        "diferencia_potencial",
        "ratio_valor_salario",
        "anos_contrato_restantes",
        # Demografía
        "edad"
    ]
    
    # Columnas categóricas (ORDEN EXACTO del entrenamiento)
    col_categoricas = [
        "categoria_posicion",
        "categoria_edad",
        "pie_preferido",
        "categoria_reputacion",
        "liga"
    ]
    
    # Crear DataFrame con todas las columnas necesarias (inicializadas con valores por defecto)
    df_completo = pd.DataFrame(index=df_input.index)
    
    # Copiar columnas numéricas disponibles
    for col in col_numericas:
        if col in df_input.columns:
            df_completo[col] = df_input[col]
        else:
            # Imputar con mediana del dataset si no está disponible
            if col in df_jugadores.columns:
                df_completo[col] = df_jugadores[col].median()
            else:
                df_completo[col] = 0
    
    # Copiar columnas categóricas disponibles
    for col in col_categoricas:
        if col in df_input.columns:
            df_completo[col] = df_input[col]
        else:
            # Imputar con moda del dataset si no está disponible
            if col in df_jugadores.columns:
                df_completo[col] = df_jugadores[col].mode()[0]
            else:
                # Valores por defecto
                if col == "categoria_posicion":
                    df_completo[col] = "Mediocampista"
                elif col == "categoria_edad":
                    df_completo[col] = "Prime"
                elif col == "pie_preferido":
                    df_completo[col] = "Right"
                elif col == "categoria_reputacion":
                    df_completo[col] = "Regional"
                elif col == "liga":
                    df_completo[col] = "English Premier League"
    
    # Extraer features numéricas
    X_num = df_completo[col_numericas].copy()
    
    # Target Encoding para club (si está disponible)
    if "club" in df_input.columns and df_input["club"].notna().any():
        club_valor = club_encoding.get(
            df_input["club"].iloc[0], 
            df_jugadores["valor_mercado_eur"].mean()
        )
        X_num["club_valor_promedio"] = club_valor
    else:
        # Si no hay club, usar promedio general
        X_num["club_valor_promedio"] = df_jugadores["valor_mercado_eur"].mean()
    
    # OneHot Encoding para categóricas
    X_cat = df_completo[col_categoricas]
    X_cat_encoded = encoder.transform(X_cat)
    col_encoded_nombres = encoder.get_feature_names_out(col_categoricas)
    X_cat_df = pd.DataFrame(
        X_cat_encoded, 
        columns=col_encoded_nombres, 
        index=df_completo.index
    )
    
    # Concatenar numéricas + categóricas
    X_final = pd.concat(
        [X_num.reset_index(drop=True), X_cat_df.reset_index(drop=True)], 
        axis=1
    )
    
    return X_final


def imputar_valores_faltantes(df_input):
    """
    Imputa valores faltantes con medianas/modas del dataset original.
    """
    columnas_numericas = df_input.select_dtypes(include=[np.number]).columns
    columnas_categoricas = df_input.select_dtypes(include=["object"]).columns
    
    # Imputar numéricas con mediana
    for col in columnas_numericas:
        if col in df_jugadores.columns and df_input[col].isnull().any():
            df_input[col].fillna(df_jugadores[col].median(), inplace=True)
    
    # Imputar categóricas con moda
    for col in columnas_categoricas:
        if col in df_jugadores.columns and df_input[col].isnull().any():
            df_input[col].fillna(df_jugadores[col].mode()[0], inplace=True)
    
    return df_input


def calcular_predicciones_dataset():
    """
    Calcula predicciones para una muestra del dataset de forma optimizada.
    Usa predicción en lote (batch) en lugar de fila por fila.
    """
    # Usar muestra más pequeña (2000 jugadores) para respuesta más rápida
    # En producción, las predicciones deberían estar pre-calculadas
    sample_size = min(2000, len(df_jugadores))
    df_sample = df_jugadores.sample(sample_size, random_state=42).copy()
    
    try:
        # Preparar datos en lote (mucho más rápido que fila por fila)
        X_batch = preparar_datos_para_prediccion_api(df_sample)
        
        # Predicción en lote
        valores_log = modelo.predict(X_batch)
        valores_eur = np.expm1(valores_log)
        
        df_sample["valor_predicho_eur"] = valores_eur
        
    except Exception as e:
        print(f"Error en predicción en lote: {str(e)}")
        # Fallback: predicción fila por fila (más lento pero más robusto)
        predicciones = []
        for idx, row in df_sample.iterrows():
            try:
                X_pred = preparar_datos_para_prediccion(row)
                valor_log = modelo.predict(X_pred)[0]
                valor_eur = np.expm1(valor_log)
                predicciones.append(valor_eur)
            except:
                predicciones.append(np.nan)
        
        df_sample["valor_predicho_eur"] = predicciones
    
    return df_sample


# ============================================================================
# ENDPOINT RAÍZ
# ============================================================================

@app.get("/", summary="Información de la API")
def raiz():
    """
    Endpoint raíz que retorna información sobre la API.
    """
    return {
        "nombre": "API Sistema Scouting Inteligente FIFA",
        "version": "2.0.0",
        "descripcion": "API REST para análisis y predicción de valor de mercado de jugadores de fútbol",
        "modelo_ml": {
            "tipo": "Random Forest Regressor",
            "r2_score": 0.9830,
            "features": 110,
            "jugadores_entrenamiento": 91875
        },
        "endpoints_disponibles": {
            "filtros": "/jugadores/filtros",
            "buscar": "/jugadores/buscar",
            "perfil": "/jugadores/{jugador_id}/perfil",
            "predecir": "/ml/predecir_valor",
            "infravalorados": "/jugadores/infravalorados",
            "sobrevalorados": "/jugadores/sobrevalorados",
            "estadisticas": "/eda/estadisticas_generales",
            "graficos": "/eda/datos_graficos",
            "documentacion": "/docs"
        },
        "dataset": {
            "total_jugadores": len(df_jugadores),
            "total_clubes": df_jugadores["club"].nunique(),
            "total_ligas": df_jugadores["liga"].nunique()
        }
    }


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("INICIANDO API SISTEMA SCOUTING FIFA")
    print("="*80)
    print(f"Modelo cargado: R² = 98.30%")
    print(f"Dataset: {len(df_jugadores):,} jugadores")
    print(f"Servidor: http://localhost:8000")
    print(f"Documentación: http://localhost:8000/docs")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
