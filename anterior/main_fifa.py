# libreria general
import os
import pandas as pd

# funciones de los scripts
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

# ruta absoluta de la carpeta donde está el script (.../scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# construir la ruta del archivo excel de data
DATA_PATH = os.path.join(SCRIPT_DIR, ".", "data", "dataset.xlsx")

# nueva ruta de salida
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data")
PROCESSED_DATA_PATH = os.path.join(OUTPUT_DIR, "jugadores_fifa_limpio.csv")

# diccionario de hojas del excel FIFA con sus años correspondientes
HOJAS_FIFA = {
    "FIFA 15": 2015,
    "FIFA 16": 2016,
    "FIFA 17": 2017,
    "FIFA 18": 2018,
    "FIFA 19": 2019,
    "FIFA 20": 2020,
    "FIFA 21": 2021
}

# ¿este archivo se está ejecutando directamente por el usuario o está siendo importado por otro script?
if __name__ == "__main__":
    # indica dónde está el script actual
    print("="*70)
    print("PIPELINE DE LIMPIEZA - DATASET FIFA 15-21")
    print("="*70)
    print(f"\nEjecutando script desde: {os.path.abspath(__file__)}")
    
    # cargar todas las hojas del excel
    dict_dataframes = cargar_datos_excel(DATA_PATH, list(HOJAS_FIFA.keys()))

    if dict_dataframes is not None:
        # lista para almacenar dataframes limpios de cada año
        lista_dfs_limpios = []
        
        # procesar cada hoja (cada año de FIFA)
        for nombre_hoja, anio in HOJAS_FIFA.items():
            print(f"\n{'='*70}")
            print(f"PROCESANDO: {nombre_hoja} (Año {anio})")
            print(f"{'='*70}")
            
            # obtener dataframe de este año
            df_anio = dict_dataframes[nombre_hoja].copy()
            print(f"Dimensiones iniciales: {df_anio.shape}")
            
            # aplicar pipeline de limpieza
            print("\n[FASE 1] Limpieza de nombres de columnas...")
            df_anio = limpieza_nombres_columnas(df_anio)
            
            print("[FASE 2] Conversión de edad a Int64...")
            df_anio = convertir_edad_int(df_anio)
            
            print("[FASE 3] Limpieza de valores monetarios...")
            df_anio = limpieza_valores_monetarios(df_anio)
            
            print("[FASE 4] Eliminación de filas con información faltante...")
            df_anio = eliminar_filas_info_faltantes(df_anio)
            
            print("[FASE 5] Rellenando valores NaN en club...")
            df_anio = rellenar_valores_club(df_anio)
            
            print(f"[FASE 6] Agregando columna año ({anio})...")
            df_anio = agregar_columna_anio(df_anio, anio)
            
            print("[FASE 7] Eliminando jugadores duplicados...")
            df_anio = eliminar_duplicados(df_anio)
            
            print("[FASE 8] Validando rangos numéricos...")
            df_anio = validar_rangos_numericos(df_anio)
            
            print(f"\n✓ {nombre_hoja} procesado: {df_anio.shape}")
            
            # agregar a la lista
            lista_dfs_limpios.append(df_anio)
        
        # concatenar todos los dataframes
        print(f"\n{'='*70}")
        print("CONCATENANDO TODOS LOS AÑOS...")
        print(f"{'='*70}")
        
        df_final = pd.concat(lista_dfs_limpios, ignore_index=True)
        
        print(f"\nDataFrame final concatenado: {df_final.shape}")
        print(f"Años incluidos: {sorted(df_final['anio'].unique())}")
        print(f"Total de jugadores: {len(df_final)}")
        
        # eliminar duplicados globales (un jugador puede aparecer en múltiples años)
        print("\nEliminando duplicados globales (por sofifa_id y anio)...")
        df_final = df_final.drop_duplicates(subset=['sofifa_id', 'anio'], keep='first')
        df_final = df_final.reset_index(drop=True)
        print(f"DataFrame final sin duplicados: {df_final.shape}")
        
        # guardar archivo limpio
        print(f"\n{'='*70}")
        print("GUARDANDO ARCHIVO LIMPIO...")
        print(f"{'='*70}")
        
        # crear carpeta si no existe
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # guardar csv
        df_final.to_csv(PROCESSED_DATA_PATH, index=False, encoding='utf-8')
        print(f"\n✓ Archivo guardado exitosamente en: {PROCESSED_DATA_PATH}")
        
        # mostrar estadísticas finales
        print(f"\n{'='*70}")
        print("ESTADÍSTICAS FINALES")
        print(f"{'='*70}")
        print(f"\nDimensiones: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        print(f"\nDistribución por año:")
        print(df_final['anio'].value_counts().sort_index())
        print(f"\nEstadísticas generales:")
        print(f"  Edad promedio: {df_final['age'].mean():.1f} años")
        print(f"  Overall promedio: {df_final['overall'].mean():.1f}")
        print(f"  Valor de mercado promedio: €{df_final['valor_mercado'].mean():,.0f}")
        print(f"  Salario promedio: €{df_final['salario'].mean():,.0f}")
        print(f"\nTop 5 clubes con más jugadores:")
        print(df_final['club'].value_counts().head())
        
        print(f"\n{'='*70}")
        print("✓ PIPELINE COMPLETADO EXITOSAMENTE")
        print(f"{'='*70}")
                   
    else: 
        print("\n✗ Ha ocurrido un error en la carga de datos")