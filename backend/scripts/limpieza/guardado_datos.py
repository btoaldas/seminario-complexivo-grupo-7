"""
Módulo de Guardado de Datos
Sistema de Scouting FIFA
"""

import pandas as pd
import os


def guardar_datos_limpios(df, ruta_salida):
   """
   Guarda el DataFrame procesado en archivo CSV.
   
   Args:
   df: DataFrame a guardar
   ruta_salida: Ruta donde guardar el archivo
   
   Returns:
   None
   """
   print("\n" + "-"*60)
   print("GUARDANDO DATOS LIMPIOS")
   print("-"*60)
   
   # Crear directorio si no existe
   directorio = os.path.dirname(ruta_salida)
   if directorio and not os.path.exists(directorio):
       os.makedirs(directorio)
       print(f"   Directorio creado: {directorio}")
   
   # Guardar CSV
   print(f"   Guardando archivo...")
   df.to_csv(ruta_salida, index=False, encoding='utf-8')
   
   # Información del archivo guardado
   tamaño_mb = os.path.getsize(ruta_salida) / (1024 * 1024)
   
   print(f"\n   Archivo guardado exitosamente")
   print(f"   📁 Ruta: {ruta_salida}")
   print(f"   Registros: {df.shape[0]:,}")
   print(f"   Columnas: {df.shape[1]}")
   print(f"   💾 Tamaño: {tamaño_mb:.2f} MB")
   print("-"*60)
