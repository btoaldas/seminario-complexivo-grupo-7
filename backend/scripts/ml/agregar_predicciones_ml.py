"""
Script para agregar predicciones ML al dataset existente
Usa el modelo ya entrenado (modelo_fifa.joblib) para evitar re-entrenar
"""
import os
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import shutil

# Rutas (ahora el script está en backend/scripts/ml/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Subir 3 niveles: ml -> scripts -> backend -> proyecto
BACKEND_DIR = os.path.join(BASE_DIR, "..", "..")
DATA_PATH = os.path.join(BACKEND_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BACKEND_DIR, "..", "datos", "modelos")

print("\n" + "=" * 80)
print("AGREGAR PREDICCIONES ML AL DATASET FIFA")
print("=" * 80)

# 1. Cargar modelo, encoder, club_encoding
print("\n[1/4] CARGANDO MODELOS Y ENCODERS")
print("-" * 80)

modelo_path = os.path.join(MODEL_DIR, 'modelo_fifa.joblib')
encoder_path = os.path.join(MODEL_DIR, 'encoder_fifa.joblib')
club_encoding_path = os.path.join(MODEL_DIR, 'club_encoding_fifa.joblib')

print(f"⏳ Cargando modelo (modo lazy con mmap)...")
modelo = joblib.load(modelo_path, mmap_mode='r')
print(f"✓ Modelo cargado: {type(modelo).__name__}")

encoder = joblib.load(encoder_path)
print(f"✓ Encoder cargado: {type(encoder).__name__}")

club_encoding = joblib.load(club_encoding_path)
print(f"✓ Club encoding cargado: {len(club_encoding)} clubes")

# 2. Cargar dataset
print("\n[2/4] CARGANDO DATASET")
print("-" * 80)
df = pd.read_csv(DATA_PATH, low_memory=False)
print(f"✓ Dataset cargado: {df.shape[0]:,} × {df.shape[1]} columnas")

# 3. Preparar features
print("\n[3/4] PREPARANDO FEATURES Y GENERANDO PREDICCIONES")
print("-" * 80)

feature_cols_numeric = [
    'overall', 'potential', 'age', 'height_cm', 'weight_kg',
    'international_reputation', 'weak_foot', 'skill_moves',
    'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic'
]

feature_cols_categorical = [
    'preferred_foot', 'work_rate', 'body_type', 'club_name', 'league_name'
]

# Target encoding para club
df['club_encoded'] = df['club_name'].map(club_encoding).fillna(0)

# Features numéricas + club_encoded
X_numeric = df[feature_cols_numeric + ['club_encoded']].values

# Features categóricas (sin club_name)
cats_sin_club = [c for c in feature_cols_categorical if c != 'club_name']
X_categorical = df[cats_sin_club]

# OneHot encoding
X_cat_encoded = encoder.transform(X_categorical)
if hasattr(X_cat_encoded, 'toarray'):
    X_cat_encoded = X_cat_encoded.toarray()

# Concatenar
X_final = np.hstack([X_numeric, X_cat_encoded])

print(f"✓ Features preparadas: {X_final.shape}")
print(f"⏳ Generando predicciones para {len(df):,} jugadores...")

# PREDECIR
predicciones_log = modelo.predict(X_final)
predicciones_eur = np.expm1(predicciones_log)

print(f"✓ Predicciones generadas")

# Calcular diferencias y clasificar
tolerancia = 8.0
df['valor_predicho_eur'] = predicciones_eur
df['diferencia_porcentual'] = (
    (df['value_eur'] - df['valor_predicho_eur']) / 
    df['valor_predicho_eur'] * 100
)
df['tolerancia_porcentaje'] = tolerancia

def clasificar(dif):
    if dif > tolerancia:
        return "INFRAVALORADO"
    elif dif < -tolerancia:
        return "SOBREVALORADO"
    else:
        return "JUSTO"

df['clasificacion_ml'] = df['diferencia_porcentual'].apply(clasificar)

print(f"✓ Clasificación ML aplicada")
print(f"   💎 INFRAVALORADOS: {(df['clasificacion_ml'] == 'INFRAVALORADO').sum():,}")
print(f"   ⚠️  SOBREVALORADOS: {(df['clasificacion_ml'] == 'SOBREVALORADO').sum():,}")
print(f"   ✓  JUSTOS:         {(df['clasificacion_ml'] == 'JUSTO').sum():,}")

# 4. Guardar
print("\n[4/4] GUARDANDO DATASET ACTUALIZADO")
print("-" * 80)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = DATA_PATH.replace('.csv', f'_backup_{timestamp}.csv')
shutil.copy2(DATA_PATH, backup_path)
print(f"💾 Backup guardado: {os.path.basename(backup_path)}")

# Guardar CSV actualizado
df.to_csv(DATA_PATH, index=False)
print(f"✅ CSV actualizado: {DATA_PATH}")

print("\n" + "=" * 80)
print("PREDICCIONES ML AGREGADAS EXITOSAMENTE")
print("=" * 80)
print(f"Nuevas columnas agregadas:")
print(f"  - valor_predicho_eur")
print(f"  - diferencia_porcentual")
print(f"  - clasificacion_ml")
print(f"  - tolerancia_porcentaje")
print("\n✅ El dataset está listo para el API con clasificaciones ML precalculadas")
print("=" * 80 + "\n")
