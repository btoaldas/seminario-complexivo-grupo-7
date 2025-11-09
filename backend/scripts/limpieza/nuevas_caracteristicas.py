"""
Módulo de Ingeniería de Características
Sistema de Scouting FIFA
"""

import pandas as pd
import numpy as np


def crear_calidad_promedio(df):
   """
   Crea feature 'calidad_promedio' basada en atributos principales.
   Promedio de: pace, shooting, passing, dribbling, defending, physic
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   print("-"*60)
   print("   Creando 'calidad_promedio'...")
   
   df_nuevo = df.copy()
   
   # Atributos principales (YA están en español desde el renombrado)
   atributos = ['ritmo_velocidad', 'tiro_disparo', 'pase', 'regate_gambeta', 'defensa', 'fisico']
   
   df_nuevo['calidad_promedio'] = df_nuevo[atributos].mean(axis=1)
   promedio_global = df_nuevo['calidad_promedio'].mean()
   print(f"   Basado en {len(atributos)} atributos")
   print(f"   Promedio global: {promedio_global:.2f}")
   
   return df_nuevo


def crear_diferencia_potencial(df):
   """
   Crea feature 'diferencia_potencial' (potential - overall).
   Indica cuánto margen de crecimiento tiene el jugador.
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   print("-"*60)
   print("   Creando 'diferencia_potencial'...")
   
   df_nuevo = df.copy()
   
   # Columnas (YA están en español desde el renombrado)
   df_nuevo['diferencia_potencial'] = df_nuevo['potencial'] - df_nuevo['valoracion_global']
   promedio_dif = df_nuevo['diferencia_potencial'].mean()
   max_dif = df_nuevo['diferencia_potencial'].max()
   print(f"   Diferencia promedio: {promedio_dif:.2f}")
   print(f"   Diferencia máxima: {max_dif:.0f}")
   
   return df_nuevo


def crear_categoria_edad(df):
   """
   Crea feature 'categoria_edad' (joven/prime/veterano).
   - Joven: <= 23 años
   - Prime: 24-30 años
   - Veterano: > 30 años
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   print("-"*60)
   print("   Creando 'categoria_edad'...")
   
   df_nuevo = df.copy()
   
   # Columna edad (YA está en español desde el renombrado)
   df_nuevo['categoria_edad'] = pd.cut(
   df_nuevo['edad'],
   bins=[0, 23, 30, 100],
   labels=['Joven', 'Prime', 'Veterano']
   )
   
   # Mostrar distribución
   distribucion = df_nuevo['categoria_edad'].value_counts()
   print(f"   Distribución:")
   for categoria, count in distribucion.items():
       porcentaje = (count / len(df_nuevo)) * 100
       print(f"   {categoria}: {count:,} ({porcentaje:.1f}%)")
   
   return df_nuevo


def crear_categoria_posicion(df):
   """
   Crea feature 'categoria_posicion' simplificada.
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   df_nuevo = df.copy()
   
   # Columna posiciones (YA está en español desde el renombrado)
   def categorizar_posicion(posiciones):
       if pd.isna(posiciones) or posiciones == 'Desconocido':
           return 'Desconocido'
       
       posiciones_str = str(posiciones).upper()
       
       if 'GK' in posiciones_str:
           return 'Portero'
       elif any(x in posiciones_str for x in ['CB', 'LB', 'RB', 'LWB', 'RWB']):
           return 'Defensa'
       elif any(x in posiciones_str for x in ['CM', 'CDM', 'CAM', 'LM', 'RM']):
           return 'Mediocampista'
       elif any(x in posiciones_str for x in ['ST', 'CF', 'LW', 'RW']):
           return 'Delantero'
       else:
           return 'Otro'
   
   df_nuevo['categoria_posicion'] = df_nuevo['posiciones_jugador'].apply(categorizar_posicion)
   
   print(f"   Feature 'categoria_posicion' creada")
   
   return df_nuevo


def crear_ratio_valor_salario(df):
   """
   Crea feature 'ratio_valor_salario' normalizado anualmente.
   Formula: valor_mercado_eur / (salario_semanal_eur * 52 semanas)
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   df_nuevo = df.copy()
   
   # Columnas monetarias (YA están en español desde el renombrado)
   # Convertir salario semanal a anual (52 semanas) y calcular ratio
   # Evitar división por cero
   df_nuevo['ratio_valor_salario'] = np.where(
       df_nuevo['salario_eur'] > 0,
       df_nuevo['valor_mercado_eur'] / (df_nuevo['salario_eur'] * 52),
       0
   )
   
   print(f"   Feature 'ratio_valor_salario' creada (normalizado anualmente)")
   
   return df_nuevo


def crear_anos_contrato_restantes(df):
   """
   Calcula los años de contrato restantes basado en contract_valid_until.
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   print("-"*60)
   print("   Creando 'anos_contrato_restantes'...")
   
   df_nuevo = df.copy()
   
   # Obtener el año actual del dataset (máximo año presente)
   if 'ano_datos' in df_nuevo.columns:
       ano_actual = df_nuevo['ano_datos'].max()
   else:
       ano_actual = 2021  # Por defecto FIFA 21
   
   # Calcular años restantes
   df_nuevo['anos_contrato_restantes'] = np.where(
       df_nuevo['contrato_valido_hasta'].notna(),
       np.maximum(0, df_nuevo['contrato_valido_hasta'] - ano_actual),
       0
   )
   
   promedio = df_nuevo['anos_contrato_restantes'].mean()
   print(f"   Años restantes promedio: {promedio:.2f}")
   
   return df_nuevo


def crear_categoria_reputacion(df):
   """
   Categoriza international_reputation en rangos.
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con nueva columna
   """
   print("-"*60)
   print("   Creando 'categoria_reputacion'...")
   
   df_nuevo = df.copy()
   
   def categorizar_reputacion(rep):
       if pd.isna(rep):
           return 'Desconocida'
       elif rep == 1:
           return 'Local'
       elif rep == 2:
           return 'Regional'
       elif rep == 3:
           return 'Nacional'
       elif rep == 4:
           return 'Continental'
       elif rep == 5:
           return 'Mundial'
       else:
           return 'Desconocida'
   
   df_nuevo['categoria_reputacion'] = df_nuevo['reputacion_internacional'].apply(categorizar_reputacion)
   
   print(f"   Feature 'categoria_reputacion' creada")
   print(f"   Distribución:")
   dist = df_nuevo['categoria_reputacion'].value_counts()
   for cat, count in dist.items():
       print(f"      {cat}: {count:,} jugadores")
   
   return df_nuevo
