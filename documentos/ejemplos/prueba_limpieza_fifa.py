"""
Script de prueba para validar las funciones de limpieza del dataset FIFA
Prueba cada función individualmente con datos de FIFA 21
"""

import pandas as pd
from scripts_fifa.data_loader import cargar_datos_excel
from scripts_fifa.data_cleaning import (
    limpieza_nombres_columnas,
    convertir_edad_int,
    limpieza_valores_monetarios,
    eliminar_filas_info_faltantes,
    rellenar_valores_club,
    agregar_columna_anio,
    eliminar_duplicados,
    validar_rangos_numericos
)

print("="*70)
print("PRUEBA DE FUNCIONES DE LIMPIEZA - DATASET FIFA")
print("="*70)

# cargar solo una hoja para prueba rápida
DATA_PATH = "data/dataset.xlsx"
HOJA_PRUEBA = ["FIFA 21"]

print("\n[1] CARGANDO DATOS...")
dict_dataframes = cargar_datos_excel(DATA_PATH, HOJA_PRUEBA)
df_prueba = dict_dataframes["FIFA 21"].copy()

print(f"Dimensiones iniciales: {df_prueba.shape}")
print(f"Columnas originales (primeras 10): {list(df_prueba.columns[:10])}")
print(f"\nEjemplo de datos antes de limpieza:")
print(df_prueba[['short_name', 'age', 'club_name', 'value_eur', 'wage_eur']].head(3))

# Fase 1: Limpieza de nombres
print("\n" + "="*70)
print("[2] PROBANDO: limpieza_nombres_columnas()")
print("="*70)
df_prueba = limpieza_nombres_columnas(df_prueba)
print(f"Columnas renombradas (primeras 10): {list(df_prueba.columns[:10])}")

# Fase 2: Conversión de edad
print("\n" + "="*70)
print("[3] PROBANDO: convertir_edad_int()")
print("="*70)
print(f"Tipo de 'age' antes: {df_prueba['age'].dtype}")
df_prueba = convertir_edad_int(df_prueba)
print(f"Tipo de 'age' después: {df_prueba['age'].dtype}")

# Fase 3: Limpieza de valores monetarios
print("\n" + "="*70)
print("[4] PROBANDO: limpieza_valores_monetarios()")
print("="*70)
print(f"Valores monetarios antes:")
print(f"  valor_mercado - Tipo: {df_prueba['valor_mercado'].dtype}")
print(f"  salario - Tipo: {df_prueba['salario'].dtype}")
df_prueba = limpieza_valores_monetarios(df_prueba)
print(f"Valores monetarios después:")
print(f"  valor_mercado - Tipo: {df_prueba['valor_mercado'].dtype}")
print(f"  salario - Tipo: {df_prueba['salario'].dtype}")

# Fase 4: Eliminar filas con info faltante
print("\n" + "="*70)
print("[5] PROBANDO: eliminar_filas_info_faltantes()")
print("="*70)
filas_antes = len(df_prueba)
df_prueba = eliminar_filas_info_faltantes(df_prueba)
filas_despues = len(df_prueba)
print(f"Filas eliminadas: {filas_antes - filas_despues}")

# Fase 5: Rellenar clubes sin valor
print("\n" + "="*70)
print("[6] PROBANDO: rellenar_valores_club()")
print("="*70)
nans_antes = df_prueba['club'].isna().sum()
print(f"NaNs en 'club' antes: {nans_antes}")
df_prueba = rellenar_valores_club(df_prueba)
nans_despues = df_prueba['club'].isna().sum()
print(f"NaNs en 'club' después: {nans_despues}")

# Fase 6: Agregar columna año
print("\n" + "="*70)
print("[7] PROBANDO: agregar_columna_anio()")
print("="*70)
df_prueba = agregar_columna_anio(df_prueba, 2021)
print(f"Columna 'anio' agregada. Valor único: {df_prueba['anio'].unique()}")

# Fase 7: Eliminar duplicados
print("\n" + "="*70)
print("[8] PROBANDO: eliminar_duplicados()")
print("="*70)
df_prueba = eliminar_duplicados(df_prueba)

# Fase 8: Validar rangos numéricos
print("\n" + "="*70)
print("[9] PROBANDO: validar_rangos_numericos()")
print("="*70)
df_prueba = validar_rangos_numericos(df_prueba)

# Resumen final
print("\n" + "="*70)
print("RESUMEN FINAL")
print("="*70)
print(f"Dimensiones finales: {df_prueba.shape}")
print(f"\nPrimeras 5 filas del dataset limpio:")
print(df_prueba[['nombre', 'age', 'posicion', 'club', 'overall', 'potential', 
                'valor_mercado', 'salario', 'anio']].head())

print(f"\nEstadísticas de columnas clave:")
print(f"  Edad - Min: {df_prueba['age'].min()}, Max: {df_prueba['age'].max()}, Media: {df_prueba['age'].mean():.1f}")
print(f"  Overall - Min: {df_prueba['overall'].min()}, Max: {df_prueba['overall'].max()}, Media: {df_prueba['overall'].mean():.1f}")
print(f"  Valor mercado - Media: €{df_prueba['valor_mercado'].mean():,.0f}")
print(f"  Salario - Media: €{df_prueba['salario'].mean():,.0f}")

print("\n" + "="*70)
print("✓ TODAS LAS FUNCIONES PROBADAS EXITOSAMENTE")
print("="*70)
