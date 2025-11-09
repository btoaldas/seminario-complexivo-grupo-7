"""
Módulo de Carga de Datos
Sistema de Scouting FIFA
"""

import pandas as pd


def cargar_datos_fifa(ruta_archivo):
   """
   Carga TODAS las hojas del archivo Excel FIFA y las une en un solo DataFrame.
   Agrega columna 'año_datos' para identificar de qué versión FIFA viene cada registro.
   
   Args:
   ruta_archivo: Ruta al archivo Excel con datos FIFA
   
   Returns:
   DataFrame unificado con todas las hojas
   """
   print("\n" + "="*60)
   print("CARGANDO DATOS FIFA")
   print("="*60)
   print(f"Archivo: {ruta_archivo}\n")
   
   # Leer archivo Excel
   xl = pd.ExcelFile(ruta_archivo)
   
   print(f"Hojas encontradas: {len(xl.sheet_names)}")
   for sheet in xl.sheet_names:
       print(f"   - {sheet}")
   
   print("\nProcesando hojas...")
   
   dataframes = []
   
   for sheet_name in xl.sheet_names:
       print(f"\n   Cargando {sheet_name}...", end=" ")
       
       # Leer hoja
       df_temp = pd.read_excel(xl, sheet_name=sheet_name)
       
       # Extraer año del nombre de la hoja (ej: "FIFA 21" -> 2021)
       try:
           año = int(sheet_name.split()[-1])
           año_completo = 2000 + año if año < 100 else año
       except:
           año_completo = 0  # Si no se puede extraer
       
       # Agregar columna de año
       df_temp['año_datos'] = año_completo
       
       dataframes.append(df_temp)
       
       print(f"OK - {len(df_temp):,} jugadores")
   
   # Unir todos los DataFrames
   print("\nUniendo todas las hojas...")
   df_unificado = pd.concat(dataframes, ignore_index=True)
   
   print("\n" + "="*60)
   print("DATOS CARGADOS EXITOSAMENTE")
   print("="*60)
   print(f"Total jugadores: {len(df_unificado):,}")
   print(f"Total columnas: {len(df_unificado.columns)}")
   print(f"Años incluidos: {sorted(df_unificado['año_datos'].unique())}")
   print("="*60 + "\n")
   
   return df_unificado


def cargar_datos(ruta_archivo):
    """
    carga datos desde un archivo CSV o Excel
    """
    try:
        print(f"Cargando datos desde: {ruta_archivo}")
        
        if ruta_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        elif ruta_archivo.endswith('.xlsx') or ruta_archivo.endswith('.xls'):
            df = cargar_datos_fifa(ruta_archivo)
        else:
            print(f"ERROR: Formato de archivo no soportado")
            return None
            
        print(f"Datos cargados: {df.shape[0]:,} filas, {df.shape[1]} columnas")
        return df
        
    except Exception as e:
        print(f"ERROR al cargar datos: {e}")
        return None
