"""
Módulo de Imputación de Datos
Sistema de Scouting FIFA
"""

import pandas as pd
import numpy as np


def imputar_valores_nulos(df):
   """
   Imputa valores nulos de forma inteligente según el tipo de columna.
   - Numéricos: mediana
   - Categóricos: 'Desconocido'
   
   Args:
   df: DataFrame con valores nulos
   
   Returns:
   DataFrame con valores imputados
   """
   print("\n" + "-"*60)
   print(" IMPUTANDO VALORES NULOS")
   print("-"*60)
   
   df_imputado = df.copy()
   nulos_antes = df_imputado.isnull().sum().sum()
   
   print(f"  Total de nulos antes: {nulos_antes:,}")
   
   # Imputar atributos numéricos con la mediana
   columnas_numericas = df_imputado.select_dtypes(include=[np.number]).columns
   columnas_num_imputadas = 0
   
   print(f"\n   Imputando columnas numéricas ({len(columnas_numericas)})...")
   for col in columnas_numericas:
       nulos_col = df_imputado[col].isnull().sum()
       if nulos_col > 0:
           mediana = df_imputado[col].median()
           df_imputado[col].fillna(mediana, inplace=True)
           columnas_num_imputadas += 1
           if columnas_num_imputadas <= 5:
               print(f"   {col}: {nulos_col} nulos -> mediana = {mediana:.2f}")
   
   if columnas_num_imputadas > 5:
       print(f"   ... y {columnas_num_imputadas - 5} columnas más")
   
   # Imputar atributos categóricos con 'Desconocido'
   columnas_categoricas = df_imputado.select_dtypes(include=['object']).columns
   columnas_cat_imputadas = 0
   
   print(f"\n   Imputando columnas categóricas ({len(columnas_categoricas)})...")
   for col in columnas_categoricas:
       nulos_col = df_imputado[col].isnull().sum()
       if nulos_col > 0:
           df_imputado[col].fillna('Desconocido', inplace=True)
           columnas_cat_imputadas += 1
           if columnas_cat_imputadas <= 5:
               print(f"   {col}: {nulos_col} nulos -> 'Desconocido'")
   
   if columnas_cat_imputadas > 5:
       print(f"   ... y {columnas_cat_imputadas - 5} columnas más")
   
   nulos_despues = df_imputado.isnull().sum().sum()
   
   print(f"\n   Columnas numéricas imputadas: {columnas_num_imputadas}")
   print(f"   Columnas categóricas imputadas: {columnas_cat_imputadas}")
   print(f"   Total de nulos después: {nulos_despues:,}")
   print("-"*60)
   
   return df_imputado


def imputar_atributos_porteros(df):
   """
   Imputa atributos de portero en 0 para jugadores de campo.
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con atributos de portero imputados
   """
   df_imputado = df.copy()
   
   # Columnas de portero (YA están en español desde el renombrado)
   columnas_portero = [
   'gk_portero_estirada', 'gk_portero_manejo',
   'gk_portero_saque', 'gk_portero_colocacion',
   'gk_portero_reflejos'
   ]
   
   columnas_imputadas = 0
   for col in columnas_portero:
       if col in df_imputado.columns:
           df_imputado[col].fillna(0, inplace=True)
           columnas_imputadas += 1
   
   print(f"   Atributos de portero imputados: {columnas_imputadas} columnas")
   
   return df_imputado
