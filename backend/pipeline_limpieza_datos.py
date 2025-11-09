"""
Pipeline Principal de Limpieza de Datos
Sistema de Scouting FIFA

Este script ejecuta todo el pipeline de procesamiento de datos.
Procesa las 7 hojas del Excel (FIFA 15 a 21) y las unifica.
"""

import sys
sys.path.append('.')

from scripts.limpieza.cargador_datos import cargar_datos_fifa
from scripts.limpieza.renombrado_columnas import renombrar_columnas_espanol
from scripts.limpieza.limpieza_datos import (
   seleccionar_columnas_relevantes,
   eliminar_duplicados,
   eliminar_columnas_muchos_nulos,
   normalizar_valores_monetarios,
   normalizar_fechas
)
from scripts.limpieza.imputacion_datos import (
   imputar_valores_nulos,
   imputar_atributos_porteros
)
from scripts.limpieza.nuevas_caracteristicas import (
   crear_calidad_promedio,
   crear_diferencia_potencial,
   crear_categoria_edad,
   crear_categoria_posicion,
   crear_ratio_valor_salario,
   crear_anos_contrato_restantes,
   crear_categoria_reputacion
)
from scripts.limpieza.guardado_datos import guardar_datos_limpios


def main():
   """
   Función principal que ejecuta el pipeline completo de limpieza.
   """
   print("\n" + "="*70)
   print(" PIPELINE DE LIMPIEZA DE DATOS FIFA (2015-2021)")
   print("="*70)
   
   # ========================================================================
   # FASE 1: CARGA DE DATOS (Múltiples hojas)
   # ========================================================================
   print("="*70)
   print("FASE 1: CARGA DE DATOS")
   print("="*70)
   
   df = cargar_datos_fifa('../datos/originales/fifa.xlsx')
   
   if df is None:
       print("\nERROR: Error al cargar datos. Pipeline detenido.")
       return
   
   # ========================================================================
   # FASE 2: LIMPIEZA DE DATOS
   # ========================================================================
   print("\n" + "="*70)
   print("FASE 2: LIMPIEZA DE DATOS")
   print("="*70)
   
   print("\n Paso 2.1: Selección de columnas relevantes")
   df = seleccionar_columnas_relevantes(df)
   
   print("\n Paso 2.2: Renombrado de columnas a español")
   df = renombrar_columnas_espanol(df)
   
   print("\n Paso 2.3: Eliminación de duplicados (mismo jugador, mismo año)")
   df = eliminar_duplicados(df)
   
   print("\n Paso 2.4: Eliminación de columnas con exceso de nulos")
   df = eliminar_columnas_muchos_nulos(df, umbral=0.5)
   
   print("\n Paso 2.5: Normalización de valores monetarios")
   df = normalizar_valores_monetarios(df)
   
   print("\n Paso 2.6: Normalización de fechas")
   df = normalizar_fechas(df)
   
   # ========================================================================
   # FASE 3: IMPUTACIÓN DE VALORES NULOS
   # ========================================================================
   print("\n" + "="*70)
   print("FASE 3: IMPUTACIÓN DE VALORES NULOS")
   print("="*70)
   
   print("\n Paso 3.1: Imputación de valores nulos generales")
   df = imputar_valores_nulos(df)
   
   print("\n Paso 3.2: Imputación de atributos de porteros")
   df = imputar_atributos_porteros(df)
   
   # ========================================================================
   # FASE 4: FEATURE ENGINEERING
   # ========================================================================
   print("\n" + "="*70)
   print("FASE 4: INGENIERÍA DE CARACTERÍSTICAS")
   print("="*70)
   
   print("\n Paso 4.1: Calidad promedio del jugador")
   df = crear_calidad_promedio(df)
   
   print("\n Paso 4.2: Diferencia de potencial")
   df = crear_diferencia_potencial(df)
   
   print("\n Paso 4.3: Categoría de edad")
   df = crear_categoria_edad(df)
   
   print("\n Paso 4.4: Categoría de posición")
   df = crear_categoria_posicion(df)
   
   print("\n Paso 4.5: Ratio valor/salario")
   df = crear_ratio_valor_salario(df)
   
   print("\n Paso 4.6: Años de contrato restantes")
   df = crear_anos_contrato_restantes(df)
   
   print("\n Paso 4.7: Categoría de reputación internacional")
   df = crear_categoria_reputacion(df)
   
   # ========================================================================
   # FASE 5: VALIDACIÓN Y RESUMEN
   # ========================================================================
   print("\n" + "="*70)
   print("FASE 5: VALIDACIÓN Y RESUMEN FINAL")
   print("="*70)
   
   print("\n ESTADÍSTICAS FINALES:")
   print("-"*70)
   print(f"  Total de registros: {len(df):,}")
   print(f"  Total de columnas: {len(df.columns)}")
   print(f"  Valores nulos restantes: {df.isnull().sum().sum():,}")
   print(f"  Años incluidos: {sorted(df['año_datos'].unique()) if 'año_datos' in df.columns else 'N/A'}")
   print(f"  Memoria usada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
   
   # Mostrar distribución por año
   if 'año_datos' in df.columns:
       print("\n DISTRIBUCIÓN POR AÑO:")
       print("-"*70)
       for año in sorted(df['año_datos'].unique()):
           count = len(df[df['año_datos'] == año])
           print(f"  FIFA {año-2000}: {count:,} jugadores")
   
   # Mostrar columnas con más nulos (top 5)
   nulos_por_columna = df.isnull().sum()
   nulos_top = nulos_por_columna[nulos_por_columna > 0].sort_values(ascending=False).head(5)
   
   if len(nulos_top) > 0:
       print("\n  TOP 5 COLUMNAS CON MÁS NULOS:")
       print("-"*70)
       for col, count in nulos_top.items():
           porcentaje = (count / len(df)) * 100
           print(f"  {col}: {count:,} ({porcentaje:.2f}%)")
   
   print("-"*70)
   
   # ========================================================================
   # FASE 6: GUARDADO
   # ========================================================================
   print("\n" + "="*70)
   print("FASE 6: GUARDADO DE DATOS LIMPIOS")
   print("="*70)
   
   guardar_datos_limpios(df, '../datos/procesados/fifa_limpio.csv')
   
   # ========================================================================
   # FINALIZACIÓN
   # ========================================================================
   print("\n" + "="*70)
   print(" PIPELINE COMPLETADO EXITOSAMENTE")
   print("="*70)
   print("\nDatos listos para entrenamiento de modelo ML!")
   print(f"Archivo guardado: ../datos/procesados/fifa_limpio.csv")
   print("="*70 + "\n")


if __name__ == "__main__":
   main()
