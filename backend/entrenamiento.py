import os
import pandas as pd
from scripts.limpieza.cargador_datos import cargar_datos
from scripts.ml.preprocesamiento_modelo import preparar_datos_modelo, dividir_datos
from scripts.ml.entrenamiento_modelo import entrenar_y_evaluar_modelos
from scripts.ml.guardado_modelo import guardar_archivos_modelo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "datos", "modelos")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder_fifa.joblib")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_fifa.joblib")


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print("PIPELINE DE ENTRENAMIENTO OPTIMIZADO - SISTEMA SCOUTING FIFA")
    print("=" * 80)
    print("CONFIGURACIÓN BASADA EN ANÁLISIS EDA REAL:")
    print("  - Dataset: 122,501 jugadores × 73 columnas")
    print("  - Features finales: ~84 (14 numéricas + 70 categóricas)")
    print("  - Nuevas features críticas: club, liga, reputación internacional")
    print("  - Random Forest: 2000 estimadores, max_depth=30")
    print("  - Objetivo R²: > 0.65 (mejora +10-20 puntos vs modelo anterior)")
    print("=" * 80)
    
    print("\n[PASO 1/5] CARGANDO DATOS")
    print("-" * 80)
    df_clean = cargar_datos(DATA_PATH)
    
    if df_clean is not None:
        print(f"✓ Datos cargados: {df_clean.shape[0]:,} registros × {df_clean.shape[1]} columnas")
        
        print("\n[PASO 2/5] PREPROCESANDO DATOS PARA EL MODELO")
        print("-" * 80)
        X, y, encoder, club_encoding = preparar_datos_modelo(df_clean)
        
        print("\n[PASO 3/5] DIVIDIENDO DATOS (TRAIN 75% / TEST 25%)")
        print("-" * 80)
        X_train, X_test, y_train, y_test = dividir_datos(X, y)
        
        print("\n[PASO 4/5] ENTRENANDO MODELOS (Regresión Lineal + Random Forest)")
        print("-" * 80)
        modelo = entrenar_y_evaluar_modelos(X_train, X_test, y_train, y_test)
        
        print("\n[PASO 5/5] GUARDANDO MODELO, ENCODER Y CLUB ENCODING")
        print("-" * 80)
        guardar_archivos_modelo(modelo, encoder, MODEL_PATH, ENCODER_PATH, club_encoding)
        
        print("\n" + "=" * 80)
        print("ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print(f"\nArchivos generados:")
        print(f"  - Modelo:        {MODEL_PATH}")
        print(f"  - Encoder:       {ENCODER_PATH}")
        print(f"  - Club Encoding: {os.path.join(MODEL_DIR, 'club_encoding_fifa.joblib')}")
        print("\nEl modelo está listo para hacer predicciones de valor de mercado.")
        print("=" * 80 + "\n")
    else:
        print("\n" + "=" * 80)
        print("ERROR: No se pudieron cargar los datos")
        print("=" * 80 + "\n")
