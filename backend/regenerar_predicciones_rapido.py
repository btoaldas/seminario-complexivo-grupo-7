"""
Script RÁPIDO para SOLO regenerar las predicciones ML (sin entrenar modelo)
Usa el modelo YA entrenado
"""
import os
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import shutil

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "datos", "modelos")

print("\n" + "=" * 80)
print("REGENERAR PREDICCIONES ML (SIN ENTRENAR)")
print("=" * 80)

# 1. Cargar modelo, encoder, club_encoding
print("\n[1/4] CARGANDO MODELOS")
modelo = joblib.load(os.path.join(MODEL_DIR, 'modelo_fifa.joblib'), mmap_mode='r')
encoder = joblib.load(os.path.join(MODEL_DIR, 'encoder_fifa.joblib'))
club_encoding = joblib.load(os.path.join(MODEL_DIR, 'club_encoding_fifa.joblib'))
print(f"✓ Modelos cargados")

# 2. Cargar dataset
print("\n[2/4] CARGANDO DATASET")
df = pd.read_csv(DATA_PATH, low_memory=False)
print(f"✓ Dataset: {df.shape[0]:,} × {df.shape[1]} columnas")

# 3. Preparar features
print("\n[3/4] GENERANDO PREDICCIONES")

feature_cols_numeric = [
    "reputacion_internacional", "valoracion_global", "potencial", "movimiento_reacciones",
    "calidad_promedio", "pase", "mentalidad_compostura", "regate_gambeta",
    "mentalidad_vision", "tiro_disparo", "ataque_pase_corto",
    "ataque_definicion", "ataque_cabezazo", "ataque_centros", "ataque_voleas",
    "movimiento_velocidad_sprint", "movimiento_aceleracion", "movimiento_agilidad",
    "movimiento_equilibrio", "fisico",
    "defensa", "defensa_entrada_pie", "defensa_entrada_deslizante", "defensa_marcaje",
    "mentalidad_agresividad", "mentalidad_intercepciones", "mentalidad_posicionamiento",
    "mentalidad_penales", "pie_debil", "habilidades_regate", "habilidad_regate",
    "habilidad_control_balon", "habilidad_efecto", "habilidad_pase_largo",
    "habilidad_tiros_libres", "diferencia_potencial", "ratio_valor_salario",
    "anos_contrato_restantes", "edad"
]

feature_cols_categorical = [
    "categoria_posicion", "categoria_edad", "pie_preferido", "categoria_reputacion", "liga"
]

# Target encoding para club
df['club_encoded'] = df['club'].map(club_encoding).fillna(0)

# Features numéricas + club_encoded
X_numeric = df[feature_cols_numeric + ['club_encoded']].values

# Features categóricas (sin club)
cats_sin_club = [c for c in feature_cols_categorical if c != 'club']
X_categorical = df[cats_sin_club]

# OneHot encoding
X_cat_encoded = encoder.transform(X_categorical)
if hasattr(X_cat_encoded, 'toarray'):
    X_cat_encoded = X_cat_encoded.toarray()

# Concatenar
X_final = np.hstack([X_numeric, X_cat_encoded])

# PREDECIR
predicciones_log = modelo.predict(X_final)
predicciones_eur = np.expm1(predicciones_log)

# Calcular diferencias y clasificar
# LÓGICA CORRECTA: diferencia negativa = INFRAVALORADO
tolerancia = 8.0
df['valor_predicho_eur'] = predicciones_eur
df['diferencia_porcentual'] = (
    (df['valor_mercado_eur'] - df['valor_predicho_eur']) / 
    df['valor_predicho_eur'] * 100
)
df['tolerancia_porcentaje'] = tolerancia

def clasificar(dif):
    if dif < -tolerancia:
        return "INFRAVALORADO"
    elif dif > tolerancia:
        return "SOBREVALORADO"
    else:
        return "JUSTO"

df['clasificacion_ml'] = df['diferencia_porcentual'].apply(clasificar)

print(f"✓ Clasificación ML aplicada")
print(f"   💎 INFRAVALORADOS: {(df['clasificacion_ml'] == 'INFRAVALORADO').sum():,}")
print(f"   ⚠️  SOBREVALORADOS: {(df['clasificacion_ml'] == 'SOBREVALORADO').sum():,}")
print(f"   ✓  JUSTOS:         {(df['clasificacion_ml'] == 'JUSTO').sum():,}")

# 4. Guardar
print("\n[4/4] GUARDANDO")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = DATA_PATH.replace('.csv', f'_backup_{timestamp}.csv')
shutil.copy2(DATA_PATH, backup_path)
df.to_csv(DATA_PATH, index=False)
print(f"💾 Backup: {os.path.basename(backup_path)}")
print(f"✅ CSV actualizado: {DATA_PATH}")
print("=" * 80 + "\n")
