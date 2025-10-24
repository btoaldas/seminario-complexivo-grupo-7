# archivo: pipeline.py
# -*- coding: utf-8 -*-
"""
etapa 1 - pipeline de datos fifa 15–21
- lee todas las hojas del excel usando data_loader
- agrega columna año
- convierte columnas monetarias a numero
- limpia filas resumen, duplicados, nulos/imputa, selecciona columnas, guarda csv
"""

from __future__ import annotations
import os
import re
from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd

# importar el cargador de datos
from data_loader import cargar_excel_completo, obtener_ruta_dataset

# =========================
# parametros / catalogos
# =========================

# --- posiciones válidas de jugadores en el futbol ---
# este conjunto define las posiciones oficiales permitidas en fifa
# se usa para validar que los datos de posición sean coherentes
# GK = portero (goalkeeper)
# CB = defensa central, LB = lateral izquierdo, RB = lateral derecho
# LWB = lateral volante izquierdo, RWB = lateral volante derecho
# CDM = mediocampista defensivo, CM = mediocampista central, CAM = mediocampista ofensivo
# LM = mediocampista izquierdo, RM = mediocampista derecho
# LW = extremo izquierdo, RW = extremo derecho
# ST = delantero centro (striker), CF = centro delantero (center forward)
posiciones_validas = {
    "GK","CB","LB","RB","LWB","RWB", 
    "CDM","CM","CAM",
    "LM","RM","LW","RW",
    "ST","CF"
}

# --- umbral para eliminar filas con exceso de valores nulos ---
# si una fila tiene más del 90% de sus columnas vacías, se considera inútil y se elimina
# ejemplo: si una fila tiene 100 columnas y 91 están vacías (91% > 90%), se descarta
ratio_nulos_eliminar = 0.90

# --- rangos válidos para atributos numéricos clave ---
# estos rangos aseguran que los datos sean realistas y no contengan errores de captura

# rango_edad: edad mínima 14 años (juveniles), máxima 45 años (veteranos)
# jugadores fuera de este rango son considerados datos erróneos
rango_edad = (14, 45)

# rango_overall: habilidad general del jugador en escala 0-99
# valores menores a 30 indican datos corruptos o jugadores no profesionales
rango_overall = (30, 99)

# rango_potential: potencial máximo del jugador en escala 0-99
# similar a overall, valores menores a 30 son sospechosos
rango_potential = (30, 99)

# --- mapeo de nombres de columnas del dataset original a nombres estandarizados ---
# el dataset fifa viene con nombres en inglés y formatos variados entre versiones
# este diccionario traduce/normaliza los nombres para trabajar de forma consistente
# formato: 'nombre_en_dataset_original': 'nombre_estandarizado_en_español'
#
# explicación de cada mapeo:
# - short_name -> nombre: nombre corto del jugador (ej: "L. Messi")
# - age -> edad: edad del jugador en años
# - overall -> calificacion_general: calificación general de habilidad (0-99)
# - potential -> potencial: calificación de potencial futuro (0-99)
# - player_positions -> posicion: posición(es) en el campo (ej: "ST, CF")
# - club_name -> club: nombre del club actual (ej: "FC Barcelona")
# - nationality -> nacionalidad: nacionalidad del jugador (ej: "Argentina")
# - value_eur -> valor_mercado: valor de mercado en euros (numérico)
# - wage_eur -> salario: salario semanal en euros (numérico)
# - release_clause_eur -> clausula_rescision: cláusula de rescisión en euros (numérico)
mapeo_columnas = {
    'short_name': 'nombre',
    'age': 'edad', 
    'overall': 'calificacion_general',
    'potential': 'potencial',
    'player_positions': 'posicion',
    'club_name': 'club',
    'nationality': 'nacionalidad',
    'value_eur': 'valor_mercado',
    'wage_eur': 'salario',
    'release_clause_eur': 'clausula_rescision'
}

# =========================
# utilidades de reporte
# =========================
def imprimir_reporte_paso(titulo: str, filas_antes: int, filas_despues: int, detalles: str = ""):
    """
    imprime un reporte formateado de cada paso del pipeline
    muestra cuántas filas se procesaron, eliminaron o agregaron
    """
    diferencia = filas_despues - filas_antes
    porcentaje = (diferencia / filas_antes * 100) if filas_antes > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"{titulo}")
    print(f"{'='*70}")
    print(f"filas antes:   {filas_antes:,}")
    print(f"filas después: {filas_despues:,}")
    
    if diferencia > 0:
        print(f"agregadas:   {diferencia:,} filas (+{porcentaje:.2f}%)")
    elif diferencia < 0:
        print(f"eliminadas:  {abs(diferencia):,} filas ({porcentaje:.2f}%)")
    else:
        print(f"sin cambios:  0 filas")
    
    if detalles:
        print(f"\n detalles: {detalles}")
    print(f"{'='*70}")


# =========================
# utilidades i/o y año
# =========================
def leer_todas_hojas_con_anio(
    ruta_excel: str,
    mapa_hoja_anio: Dict[str, int] | None = None
) -> pd.DataFrame:
    """
    lee todas las hojas del excel usando data_loader y añade columna año.
    si mapa_hoja_anio no se provee, intenta inferir el año desde el nombre de la hoja (ej: 'fifa20' -> 2020).
    """
    # usar la funcion del data_loader para cargar las hojas
    hojas = cargar_excel_completo(ruta_excel)
    
    if hojas is None:
        raise ValueError(f"no se pudo cargar el archivo excel: {ruta_excel}")
    
    frames: List[pd.DataFrame] = []
    mapa_inferido = {}

    for nombre_hoja, df in hojas.items():
        anio = None
        if mapa_hoja_anio and nombre_hoja in mapa_hoja_anio:
            anio = mapa_hoja_anio[nombre_hoja]
        else:
            anio = inferir_anio_desde_nombre_hoja(nombre_hoja)

        if anio is None:
            raise ValueError(f"no pude inferir año para la hoja: {nombre_hoja}. "
                             "define mapa_hoja_anio={'fifa15':2015, ...}")

        mapa_inferido[nombre_hoja] = anio
        df = df.copy()
        df["anio"] = anio
        df["hoja_origen"] = nombre_hoja  # util para auditoria
        frames.append(df)

    resultado = pd.concat(frames, ignore_index=True)
    return resultado


def inferir_anio_desde_nombre_hoja(nombre: str) -> Union[int, None]:
    """
    intenta inferir año desde el nombre de hoja.
    reglas:
      - 'fifa21' -> 2021
      - '2019' -> 2019
      - '15' -> 2015 si parece fifa15
    """
    s = nombre.upper().strip()
    # buscar 'fifa' + dos digitos
    m = re.search(r"fifa\s*'?(\d{2})", s)
    if m:
        yy = int(m.group(1))
        return 2000 + yy if yy <= 30 else 1900 + yy  # por si acaso

    # buscar 4 digitos consecutivos (año)
    m = re.search(r"\b(20\d{2})\b", s)
    if m:
        return int(m.group(1))

    # buscar dos digitos sueltos
    m = re.search(r"\b(\d{2})\b", s)
    if m:
        yy = int(m.group(1))
        return 2000 + yy if yy <= 30 else 1900 + yy

    return None


def renombrar_columnas_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    renombra las columnas del dataset real a nombres estandarizados
    """
    df_resultado = df.copy()
    
    # renombrar solo las columnas que existen en el dataframe
    columnas_a_renombrar = {}
    for col_original, col_nueva in mapeo_columnas.items():
        if col_original in df_resultado.columns:
            columnas_a_renombrar[col_original] = col_nueva
    
    df_resultado = df_resultado.rename(columns=columnas_a_renombrar)
    return df_resultado


# =========================
# conversion de montos a numero
# =========================
def convertir_dinero_a_numero(x) -> Union[float, None]:
    """
    convierte números que ya vienen en euros (eur) a float.
    el dataset fifa ya tiene valores numericos en euros, no strings como '€2.5m'.
    maneja casos nulos y no numericos.
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)

    # si es string, intentar convertir
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def agregar_columnas_dinero_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """
    procesa las columnas monetarias que ya vienen en formato numerico (eur)
    """
    resultado = df.copy()
    
    # las columnas ya están en formato numerico en el dataset fifa
    # solo necesitamos asegurar que sean float y manejar nulos
    columnas_dinero = ['valor_mercado', 'salario', 'clausula_rescision']
    
    for col in columnas_dinero:
        if col in resultado.columns:
            resultado[col] = resultado[col].apply(convertir_dinero_a_numero)
    
    return resultado


# =========================
# limpieza avanzada
# =========================
def eliminar_filas_resumen_y_fuera_rango(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    eliminar filas de totales/resumenes y filas fuera de rangos validos (edad/calificacion_general/potencial).
    retorna: (dataframe_limpio, estadisticas)
    """
    filas_iniciales = len(df)
    resultado = df.copy()
    stats = {
        'filas_iniciales': filas_iniciales,
        'eliminadas_resumen': 0,
        'eliminadas_nulos_excesivos': 0,
        'eliminadas_edad_invalida': 0,
        'eliminadas_calificacion_invalida': 0,
        'eliminadas_potencial_invalido': 0,
        'ejemplos_edad_invalida': [],
        'ejemplos_calificacion_invalida': [],
        'ejemplos_potencial_invalido': []
    }

    # 1) filas de "resumen/totales" por heuristica en nombre
    if "nombre" in resultado.columns:
        # usar grupo no-capturante (?:...) para evitar warning de pandas
        mascara_resumen = resultado["nombre"].astype(str).str.upper().str.contains(
            r"\b(?:total|sum|average|promedio|summary)\b", regex=True, na=False
        )
        stats['eliminadas_resumen'] = mascara_resumen.sum()
        resultado = resultado[~mascara_resumen]

    # 2) eliminar por % de nulos muy alto
    ratio_nulos = resultado.isna().mean(axis=1)
    mascara_nulos = ratio_nulos > ratio_nulos_eliminar
    stats['eliminadas_nulos_excesivos'] = mascara_nulos.sum()
    resultado = resultado[~mascara_nulos]

    # 3) rangos validos
    def en_rango(col, minimo, maximo):
        if col not in resultado.columns:
            return pd.Series(True, index=resultado.index)
        return (resultado[col].between(minimo, maximo)) | (~resultado[col].notna())

    # edad
    if "edad" in resultado.columns:
        mascara_edad = ~en_rango("edad", *rango_edad)
        stats['eliminadas_edad_invalida'] = mascara_edad.sum()
        # capturar ejemplos de jugadores eliminados
        if mascara_edad.sum() > 0:
            ejemplos = resultado[mascara_edad][['nombre','edad','anio']].head(3).to_dict('records')
            stats['ejemplos_edad_invalida'] = ejemplos
        resultado = resultado[en_rango("edad", *rango_edad)]
    
    # calificacion_general
    if "calificacion_general" in resultado.columns:
        mascara_cal = ~en_rango("calificacion_general", *rango_overall)
        stats['eliminadas_calificacion_invalida'] = mascara_cal.sum()
        # capturar ejemplos
        if mascara_cal.sum() > 0:
            ejemplos = resultado[mascara_cal][['nombre','calificacion_general','anio']].head(3).to_dict('records')
            stats['ejemplos_calificacion_invalida'] = ejemplos
        resultado = resultado[en_rango("calificacion_general", *rango_overall)]
    
    # potencial
    if "potencial" in resultado.columns:
        mascara_pot = ~en_rango("potencial", *rango_potential)
        stats['eliminadas_potencial_invalido'] = mascara_pot.sum()
        # capturar ejemplos
        if mascara_pot.sum() > 0:
            ejemplos = resultado[mascara_pot][['nombre','potencial','anio']].head(3).to_dict('records')
            stats['ejemplos_potencial_invalido'] = ejemplos
        resultado = resultado[en_rango("potencial", *rango_potential)]

    stats['filas_finales'] = len(resultado)
    stats['total_eliminadas'] = filas_iniciales - len(resultado)
    
    if verbose:
        detalles = (f"resumen: {stats['eliminadas_resumen']}, "
                   f"nulos excesivos: {stats['eliminadas_nulos_excesivos']}, "
                   f"edad inválida: {stats['eliminadas_edad_invalida']}, "
                   f"calificación inválida: {stats['eliminadas_calificacion_invalida']}, "
                   f"potencial inválido: {stats['eliminadas_potencial_invalido']}")
        imprimir_reporte_paso("paso 3: limpieza de filas inválidas", filas_iniciales, len(resultado), detalles)
        
        # mostrar ejemplos de jugadores eliminados
        if stats['ejemplos_edad_invalida']:
            print("\n  🔍 Ejemplos de jugadores eliminados por edad inválida:")
            for ej in stats['ejemplos_edad_invalida']:
                print(f"      • {ej['nombre']} - edad: {ej['edad']} años (año {ej['anio']})")
    
    return resultado, stats


def eliminar_y_resolver_duplicados(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    eliminar duplicados por nombre+anio quedandose con la fila 'mejor' (menos nulos, mayor calificacion_general).
    retorna: (dataframe_sin_duplicados, estadisticas)
    """
    filas_iniciales = len(df)
    resultado = df.copy()
    stats = {
        'filas_iniciales': filas_iniciales,
        'duplicados_encontrados': 0,
        'duplicados_eliminados': 0,
        'ejemplos_duplicados': []
    }
    
    if not {"nombre", "anio"}.issubset(resultado.columns):
        stats['filas_finales'] = filas_iniciales
        return resultado, stats

    # contar duplicados antes de eliminar
    duplicados_antes = resultado.duplicated(subset=["nombre", "anio"], keep=False).sum()
    stats['duplicados_encontrados'] = duplicados_antes
    
    # capturar ejemplos de duplicados ANTES de eliminar
    if duplicados_antes > 0:
        mascara_dup = resultado.duplicated(subset=["nombre", "anio"], keep=False)
        df_duplicados = resultado[mascara_dup].copy()
        # tomar el primer jugador duplicado y mostrar sus versiones
        if len(df_duplicados) > 0:
            primer_duplicado = df_duplicados.iloc[0]
            nombre_ej = primer_duplicado['nombre']
            anio_ej = primer_duplicado['anio']
            versiones = resultado[(resultado['nombre'] == nombre_ej) & (resultado['anio'] == anio_ej)]
            if len(versiones) > 1:
                ejemplos = versiones[['nombre','anio','calificacion_general','club']].head(3).to_dict('records')
                stats['ejemplos_duplicados'] = ejemplos

    # metrica de calidad por fila: menos nulos es mejor; si empata, mayor calificacion_general
    conteo_no_nulos = resultado.notna().sum(axis=1)
    calificacion_general = resultado["calificacion_general"] if "calificacion_general" in resultado.columns else pd.Series(0, index=resultado.index)

    resultado["_ranking_calidad"] = list(zip(conteo_no_nulos, calificacion_general))
    resultado.sort_values(["nombre", "anio", "_ranking_calidad"], ascending=[True, True, False], inplace=True)
    resultado = resultado.drop_duplicates(subset=["nombre", "anio"], keep="first")
    resultado = resultado.drop(columns=["_ranking_calidad"], errors="ignore")
    
    stats['filas_finales'] = len(resultado)
    stats['duplicados_eliminados'] = filas_iniciales - len(resultado)
    
    if verbose:
        detalles = f"encontrados: {stats['duplicados_encontrados']} registros duplicados, eliminados: {stats['duplicados_eliminados']}, conservando mejor calidad"
        imprimir_reporte_paso("paso 5: eliminación de duplicados", filas_iniciales, len(resultado), detalles)
        
        # mostrar ejemplo de resolución de duplicados
        if stats['ejemplos_duplicados']:
            print("\n  Ejemplo de jugador duplicado (se conserva el de mayor calificación):")
            for i, ej in enumerate(stats['ejemplos_duplicados'], 1):
                marca = "CONSERVADO" if i == 1 else " ELIMINADO"
                print(f"      {marca}: {ej['nombre']} ({ej['anio']}) - Calif: {ej.get('calificacion_general', 'N/A')} - Club: {ej.get('club', 'N/A')}")
    
    return resultado, stats


def imputar_y_llenar(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    imputar numericos clave por mediana (posicion/anio) y llenar categoricos vacios con 'desconocido'.
    retorna: (dataframe_imputado, estadisticas)
    """
    filas_iniciales = len(df)
    resultado = df.copy()
    stats = {
        'filas_iniciales': filas_iniciales,
        'nulos_antes': {},
        'nulos_despues': {},
        'valores_imputados': {},
        'ejemplos_imputacion_club': []
    }

    # registrar nulos antes
    columnas_interes = ["club", "nacionalidad", "posicion", "edad", "calificacion_general", "potencial"]
    for col in columnas_interes:
        if col in resultado.columns:
            stats['nulos_antes'][col] = resultado[col].isna().sum()

    # categoricos a desconocido - capturar ejemplos antes
    for col in ["club", "nacionalidad", "posicion"]:
        if col in resultado.columns:
            nulos = resultado[col].isna().sum()
            vacios = (resultado[col] == "").sum()
            
            # capturar ejemplos de imputación (solo para club)
            if col == "club" and nulos > 0:
                mascara_nulos = resultado[col].isna()
                ejemplos = resultado[mascara_nulos][['nombre','anio']].head(3).to_dict('records')
                stats['ejemplos_imputacion_club'] = ejemplos
            
            resultado[col] = resultado[col].fillna("desconocido").replace("", "desconocido")
            stats['valores_imputados'][col] = nulos + vacios

    # imputar numericos clave por grupo (posicion, anio) -> mediana
    def imputar_por_grupo(col: str):
        if col not in resultado.columns:
            return
        nulos_iniciales = resultado[col].isna().sum()
        
        # por posicion y anio
        resultado[col] = resultado.groupby(["posicion", "anio"], dropna=False)[col].transform(
            lambda s: s.fillna(s.median())
        )
        # fallback por anio
        resultado[col] = resultado.groupby(["anio"], dropna=False)[col].transform(
            lambda s: s.fillna(s.median())
        )
        # fallback global
        resultado[col] = resultado[col].fillna(resultado[col].median())
        
        nulos_finales = resultado[col].isna().sum()
        stats['valores_imputados'][col] = nulos_iniciales - nulos_finales

    for col in ["edad", "calificacion_general", "potencial"]:
        imputar_por_grupo(col)

    # registrar nulos después
    for col in columnas_interes:
        if col in resultado.columns:
            stats['nulos_despues'][col] = resultado[col].isna().sum()

    stats['filas_finales'] = len(resultado)
    stats['total_valores_imputados'] = sum(stats['valores_imputados'].values())
    
    if verbose:
        detalles_items = [f"{col}: {cant} valores" for col, cant in stats['valores_imputados'].items() if cant > 0]
        detalles = "imputados -> " + ", ".join(detalles_items) if detalles_items else "sin valores para imputar"
        imprimir_reporte_paso("paso 6: imputación de valores faltantes", filas_iniciales, len(resultado), detalles)
        
        # mostrar ejemplos de imputación
        if stats['ejemplos_imputacion_club']:
            print("\n  Ejemplos de jugadores sin club (se les asignó 'desconocido'):")
            for ej in stats['ejemplos_imputacion_club']:
                print(f"      • {ej['nombre']} ({ej['anio']}) - club: [vacío] → 'desconocido'")
    
    return resultado, stats


def eliminar_filas_sin_objetivo(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    eliminar filas sin objetivo (valor_mercado).
    retorna: (dataframe_filtrado, estadisticas)
    """
    filas_iniciales = len(df)
    resultado = df.copy()
    stats = {
        'filas_iniciales': filas_iniciales,
        'filas_sin_valor_mercado': 0
    }
    
    if "valor_mercado" in resultado.columns:
        stats['filas_sin_valor_mercado'] = resultado["valor_mercado"].isna().sum()
        resultado = resultado[~resultado["valor_mercado"].isna()]
    
    stats['filas_finales'] = len(resultado)
    
    if verbose:
        detalles = f"eliminadas {stats['filas_sin_valor_mercado']} filas sin valor de mercado"
        imprimir_reporte_paso("paso 7: eliminación de filas sin objetivo", filas_iniciales, len(resultado), detalles)
    
    return resultado, stats


def seleccionar_columnas_para_ml(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    seleccionar columnas minimas para el modelo inicial.
    retorna: (dataframe_con_columnas_seleccionadas, estadisticas)
    """
    columnas_iniciales = df.shape[1]
    columnas_originales = list(df.columns)
    cols = ["nombre", "anio", "edad", "calificacion_general", "potencial", "posicion", "club", "nacionalidad", "valor_mercado"]
    existentes = [c for c in cols if c in df.columns]
    resultado = df[existentes].copy()
    
    # calcular columnas eliminadas
    cols_eliminadas = [c for c in columnas_originales if c not in existentes]
    
    stats = {
        'columnas_iniciales': columnas_iniciales,
        'columnas_finales': len(existentes),
        'columnas_seleccionadas': existentes,
        'columnas_eliminadas': columnas_iniciales - len(existentes),
        'lista_eliminadas': cols_eliminadas[:10]  # primeras 10 eliminadas
    }
    
    if verbose:
        detalles = f"seleccionadas {len(existentes)} columnas: {', '.join(existentes)}"
        print(f"\n{'='*70}")
        print(f"paso 8: selección de columnas para ml")
        print(f"{'='*70}")
        print(f"  columnas antes:   {columnas_iniciales}")
        print(f"  columnas después: {len(existentes)}")
        print(f"  eliminadas:    {stats['columnas_eliminadas']} columnas")
        print(f"\n  detalles: {detalles}")
        
        # mostrar ejemplos de columnas eliminadas
        if stats['lista_eliminadas']:
            print(f"\n  Ejemplos de columnas eliminadas (primeras 10):")
            print(f"      {', '.join(stats['lista_eliminadas'][:10])}")
            if len(cols_eliminadas) > 10:
                print(f"      ... y {len(cols_eliminadas) - 10} más")
        
        print(f"{'='*70}")
    
    return resultado, stats


# =========================
# reporte de calidad
# =========================
def reporte_calidad(df_antes: pd.DataFrame, df_despues: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    retorna un mini-reporte con:
    - filas antes/despues
    - % nulos por columna
    """
    reporte = {
        "filas_antes": len(df_antes),
        "filas_despues": len(df_despues),
        "columnas_despues": df_despues.shape[1]
    }
    nulos = df_despues.isna().mean().sort_values(ascending=False).to_frame("ratio_nulos")
    resumen = pd.DataFrame([reporte])
    return resumen, nulos


# =========================
# orquestador
# =========================
def ejecutar_pipeline(ruta_excel: str, archivo_csv_salida: str = "data/dataset_limpio.csv") -> Tuple[pd.DataFrame, Dict]:
    """
    ejecuta la etapa 1 completa con reportes detallados de cada paso:
      1) leer todas las hojas + anio
      2) renombrar columnas al estandar
      3) quitar filas resumen y fuera de rango
      4) convertir monetarios
      5) quitar duplicados nombre+anio
      6) imputar/llenar
      7) eliminar filas sin objetivo (valor_mercado)
      8) seleccion de columnas
      9) guardar csv
      10) resumen final consolidado
    retorna: (df_final, estadisticas_completas)
    """
    estadisticas_globales = {}
    
    print("\n" + "="*70)
    print("iniciando pipeline de datos fifa 15-21")
    print("="*70)
    
    # paso 1: leer datos
    print("\n paso 1: cargando hojas del excel...")
    df0 = leer_todas_hojas_con_anio(ruta_excel)
    filas_iniciales_totales = len(df0)
    columnas_iniciales = df0.shape[1]
    estadisticas_globales['paso_1_carga'] = {
        'filas_cargadas': filas_iniciales_totales,
        'columnas_originales': columnas_iniciales
    }
    imprimir_reporte_paso("paso 1: carga de datos", 0, filas_iniciales_totales, 
                         f"{columnas_iniciales} columnas originales cargadas")

    # paso 2: renombrar columnas
    print("\n  paso 2: renombrando columnas al español...")
    df1 = renombrar_columnas_dataset(df0)
    columnas_renombradas = len([c for c in mapeo_columnas.values() if c in df1.columns])
    estadisticas_globales['paso_2_renombrado'] = {
        'columnas_renombradas': columnas_renombradas
    }
    print(f"  {columnas_renombradas} columnas renombradas correctamente")
    
    # paso 3: limpiar filas
    print("\n🧹 paso 3: limpiando filas inválidas...")
    df2, stats_limpieza = eliminar_filas_resumen_y_fuera_rango(df1, verbose=True)
    estadisticas_globales['paso_3_limpieza'] = stats_limpieza
    
    # paso 4: convertir monetarios
    print("\n paso 4: procesando columnas monetarias...")
    df3 = agregar_columnas_dinero_numericas(df2)
    columnas_monetarias = ['valor_mercado', 'salario', 'clausula_rescision']
    procesadas = sum(1 for c in columnas_monetarias if c in df3.columns)
    estadisticas_globales['paso_4_monetarios'] = {
        'columnas_procesadas': procesadas
    }
    print(f"  {procesadas} columnas monetarias procesadas")
    
    # paso 5: duplicados
    print("\n paso 5: resolviendo duplicados...")
    df4, stats_duplicados = eliminar_y_resolver_duplicados(df3, verbose=True)
    estadisticas_globales['paso_5_duplicados'] = stats_duplicados
    
    # paso 6: imputacion
    print("\n paso 6: imputando valores faltantes...")
    df5, stats_imputacion = imputar_y_llenar(df4, verbose=True)
    estadisticas_globales['paso_6_imputacion'] = stats_imputacion
    
    # paso 7: eliminar sin objetivo
    print("\n paso 7: filtrando por objetivo (valor_mercado)...")
    df6, stats_objetivo = eliminar_filas_sin_objetivo(df5, verbose=True)
    estadisticas_globales['paso_7_objetivo'] = stats_objetivo
    
    # paso 8: seleccion columnas
    print("\n paso 8: seleccionando columnas para ml...")
    df_final, stats_columnas = seleccionar_columnas_para_ml(df6, verbose=True)
    estadisticas_globales['paso_8_seleccion'] = stats_columnas

    # paso 9: guardar
    print(f"\n paso 9: guardando dataset en '{archivo_csv_salida}'...")
    
    # crear la carpeta de destino si no existe
    directorio_destino = os.path.dirname(archivo_csv_salida)
    if directorio_destino and not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print(f"  carpeta '{directorio_destino}' creada")
    
    df_final.to_csv(archivo_csv_salida, index=False, encoding="utf-8")
    print(f"  archivo guardado exitosamente")

    # paso 10: resumen final consolidado
    print("\n" + "="*70)
    print(" resumen final del pipeline")
    print("="*70)
    print(f"\n transformación de datos:")
    print(f"  • filas iniciales:       {filas_iniciales_totales:,}")
    print(f"  • filas finales:         {len(df_final):,}")
    print(f"  • filas eliminadas:      {filas_iniciales_totales - len(df_final):,} ({(filas_iniciales_totales - len(df_final))/filas_iniciales_totales*100:.2f}%)")
    print(f"  • columnas iniciales:    {columnas_iniciales}")
    print(f"  • columnas finales:      {df_final.shape[1]}")
    
    print(f"\n detalle de eliminaciones:")
    print(f"  • filas resumen:         {stats_limpieza['eliminadas_resumen']:,}")
    print(f"  • nulos excesivos:       {stats_limpieza['eliminadas_nulos_excesivos']:,}")
    print(f"  • edad inválida:         {stats_limpieza['eliminadas_edad_invalida']:,}")
    print(f"  • calificación inválida: {stats_limpieza['eliminadas_calificacion_invalida']:,}")
    print(f"  • potencial inválido:    {stats_limpieza['eliminadas_potencial_invalido']:,}")
    print(f"  • duplicados:            {stats_duplicados['duplicados_eliminados']:,}")
    print(f"  • sin valor mercado:     {stats_objetivo['filas_sin_valor_mercado']:,}")
    
    print(f"\n valores imputados:")
    for col, cant in stats_imputacion['valores_imputados'].items():
        if cant > 0:
            print(f"  • {col}: {cant:,} valores")
    
    print(f"\n columnas finales del dataset:")
    for i, col in enumerate(stats_columnas['columnas_seleccionadas'], 1):
        print(f"  {i}. {col}")
    
    # calidad del dataset final
    nulos_finales = df_final.isna().sum().sum()
    print(f"\n calidad del dataset final:")
    print(f"  • valores nulos totales:  {nulos_finales:,}")
    print(f"  • porcentaje nulos:       {(nulos_finales / (len(df_final) * df_final.shape[1])) * 100:.4f}%")
    print(f"  • completitud:            {100 - (nulos_finales / (len(df_final) * df_final.shape[1])) * 100:.4f}%")
    
    print("\n" + "="*70)
    print(" pipeline completado exitosamente!")
    print("="*70 + "\n")
    
    estadisticas_globales['resumen_final'] = {
        'filas_iniciales': filas_iniciales_totales,
        'filas_finales': len(df_final),
        'filas_eliminadas': filas_iniciales_totales - len(df_final),
        'porcentaje_retenido': (len(df_final) / filas_iniciales_totales) * 100,
        'columnas_finales': df_final.shape[1],
        'nulos_totales': nulos_finales,
        'porcentaje_completitud': 100 - (nulos_finales / (len(df_final) * df_final.shape[1])) * 100
    }
    
    return df_final, estadisticas_globales


if __name__ == "__main__":
    # ejecucion del pipeline usando la ruta del data_loader
    ruta_excel = obtener_ruta_dataset()
    print(f"\n usando dataset: {ruta_excel}")
    
    # ejecutar pipeline con reportes detallados
    df_final, estadisticas = ejecutar_pipeline(ruta_excel)
    
    # mostrar muestra de datos finales
    print("\n" + "="*70)
    print(" vista previa del dataset final")
    print("="*70)
    print(df_final.head(10))
    
    print("\n" + "="*70)
    print(" información del dataset")
    print("="*70)
    df_final.info()
    
    print("\n" + "="*70)
    print(" estadísticas descriptivas")
    print("="*70)
    print(df_final.describe())