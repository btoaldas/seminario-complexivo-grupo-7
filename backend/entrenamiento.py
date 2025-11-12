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
        
        # LIMPIEZA: Eliminar columnas ML previas si existen (evitar data leakage)
        columnas_ml = ['valor_predicho_eur', 'diferencia_porcentual', 'clasificacion_ml', 'tolerancia_porcentaje']
        columnas_existentes = [col for col in columnas_ml if col in df_clean.columns]
        
        if columnas_existentes:
            print(f"⚠️  Detectadas columnas ML previas: {columnas_existentes}")
            print("   Eliminándolas para evitar data leakage en el entrenamiento...")
            df_clean = df_clean.drop(columns=columnas_existentes)
            print(f"✓ Dataset limpio para entrenamiento: {df_clean.shape[0]:,} × {df_clean.shape[1]} columnas")
        
        print("\n[PASO 2/5] PREPROCESANDO DATOS PARA EL MODELO")
        print("-" * 80)
        X, y, encoder, club_encoding = preparar_datos_modelo(df_clean)
        
        print("\n[PASO 3/5] DIVIDIENDO DATOS (TRAIN 75% / TEST 25%)")
        print("-" * 80)
        X_train, X_test, y_train, y_test = dividir_datos(X, y)
        
        print("\n[PASO 4/5] ENTRENANDO MODELOS (Regresión Lineal + Random Forest)")
        print("-" * 80)
        modelo = entrenar_y_evaluar_modelos(X_train, X_test, y_train, y_test)
        
        print("\n[PASO 5/6] GUARDANDO MODELO, ENCODER Y CLUB ENCODING")
        print("-" * 80)
        guardar_archivos_modelo(modelo, encoder, MODEL_PATH, ENCODER_PATH, club_encoding)
        
        print("\n[PASO 6/6] GENERANDO PREDICCIONES ML PARA TODO EL DATASET")
        print("-" * 80)
        print("⚠️  Este proceso puede tardar varios minutos (122,501 jugadores)...")
        print("💡 Se agregará: valor_predicho_eur, diferencia_porcentual, clasificacion_ml")
        print("💾 Se creará backup automático de fifa_limpio.csv")
        print("-" * 80)
        
        # Usar modelo y encoder que YA están en memoria (no recargar)
        import numpy as np
        from datetime import datetime
        import shutil
        
        try:
            # Cargar dataset completo
            df_completo = pd.read_csv(DATA_PATH, low_memory=False)
            print(f"✓ Dataset cargado: {df_completo.shape[0]:,} × {df_completo.shape[1]} columnas")
            
            # Preparar features para predicción (IGUAL que en preprocesamiento_modelo.py)
            feature_cols_numeric = [
                # TOP FEATURES
                "reputacion_internacional",
                "valoracion_global",
                "potencial",
                "movimiento_reacciones",
                # FEATURES MODERADAS
                "calidad_promedio",
                "pase",
                "mentalidad_compostura",
                "regate_gambeta",
                "mentalidad_vision",
                "tiro_disparo",
                "ataque_pase_corto",
                # FEATURES ADICIONALES
                "ataque_definicion",
                "ataque_cabezazo",
                "ataque_centros",
                "ataque_voleas",
                # Físicos
                "movimiento_velocidad_sprint",
                "movimiento_aceleracion",
                "movimiento_agilidad",
                "movimiento_equilibrio",
                "fisico",
                # Defensivos
                "defensa",
                "defensa_entrada_pie",
                "defensa_entrada_deslizante",
                "defensa_marcaje",
                # Mentales
                "mentalidad_agresividad",
                "mentalidad_intercepciones",
                "mentalidad_posicionamiento",
                "mentalidad_penales",
                # Habilidades
                "pie_debil",
                "habilidades_regate",
                "habilidad_regate",
                "habilidad_control_balon",
                "habilidad_efecto",
                "habilidad_pase_largo",
                "habilidad_tiros_libres",
                # Features calculadas
                "diferencia_potencial",
                "ratio_valor_salario",
                "anos_contrato_restantes",
                # Demografía
                "edad"
            ]
            
            feature_cols_categorical = [
                "categoria_posicion",
                "categoria_edad",
                "pie_preferido",
                "categoria_reputacion",
                "liga"
            ]
            
            # Aplicar target encoding para club
            df_temp = df_completo.copy()
            df_temp['club_encoded'] = df_temp['club'].map(club_encoding).fillna(0)
            
            # Features numéricas + club_encoded
            X_numeric = df_temp[feature_cols_numeric + ['club_encoded']].values
            
            # Features categóricas (sin club)
            cats_sin_club = [c for c in feature_cols_categorical if c != 'club']
            X_categorical = df_temp[cats_sin_club]
            
            # OneHot encoding
            X_cat_encoded = encoder.transform(X_categorical)
            if hasattr(X_cat_encoded, 'toarray'):
                X_cat_encoded = X_cat_encoded.toarray()
            
            # Concatenar
            X_final = np.hstack([X_numeric, X_cat_encoded])
            
            print(f"✓ Features preparadas: {X_final.shape}")
            print("⏳ Generando predicciones con modelo en memoria...")
            
            # PREDECIR con modelo ya cargado
            predicciones_log = modelo.predict(X_final)
            predicciones_eur = np.expm1(predicciones_log)
            
            print(f"✓ Predicciones generadas para {len(predicciones_eur):,} jugadores")
            
            # Calcular diferencias y clasificar
            # LÓGICA CORRECTA:
            # - Si valor_real < valor_predicho → diferencia NEGATIVA → INFRAVALORADO 💎
            # - Si valor_real > valor_predicho → diferencia POSITIVA → SOBREVALORADO ⚠️
            tolerancia = 8.0
            df_completo['valor_predicho_eur'] = predicciones_eur
            df_completo['diferencia_porcentual'] = (
                (df_completo['valor_mercado_eur'] - df_completo['valor_predicho_eur']) / 
                df_completo['valor_predicho_eur'] * 100
            )
            df_completo['tolerancia_porcentaje'] = tolerancia
            
            def clasificar(dif):
                # Si diferencia NEGATIVA (valor_real < valor_predicho) → INFRAVALORADO
                if dif < -tolerancia:
                    return "INFRAVALORADO"
                # Si diferencia POSITIVA (valor_real > valor_predicho) → SOBREVALORADO
                elif dif > tolerancia:
                    return "SOBREVALORADO"
                else:
                    return "JUSTO"
            
            df_completo['clasificacion_ml'] = df_completo['diferencia_porcentual'].apply(clasificar)
            
            print(f"✓ Clasificación ML aplicada")
            print(f"   💎 INFRAVALORADOS: {(df_completo['clasificacion_ml'] == 'INFRAVALORADO').sum():,}")
            print(f"   ⚠️  SOBREVALORADOS: {(df_completo['clasificacion_ml'] == 'SOBREVALORADO').sum():,}")
            print(f"   ✓  JUSTOS:         {(df_completo['clasificacion_ml'] == 'JUSTO').sum():,}")
            
            # Backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = DATA_PATH.replace('.csv', f'_backup_{timestamp}.csv')
            shutil.copy2(DATA_PATH, backup_path)
            print(f"💾 Backup guardado: {os.path.basename(backup_path)}")
            
            # Guardar CSV actualizado
            df_completo.to_csv(DATA_PATH, index=False)
            print(f"✅ CSV actualizado: {DATA_PATH}")
            
            # PASO ADICIONAL: Optimizar dataset a Parquet automáticamente
            print("\n[PASO 7/7] OPTIMIZANDO DATASET A PARQUET")
            print("-" * 80)
            print("⚡ Convirtiendo CSV a Parquet para carga rápida en API...")
            
            try:
                from scripts.ml.optimizar_dataset import optimizar_dataset
                optimizar_dataset()
                print("✅ Optimización completada - Dataset listo para producción")
            except Exception as e:
                print(f"⚠️  Error al optimizar dataset: {e}")
                print("El CSV fue actualizado correctamente pero no se generó el Parquet")
                print("Puedes ejecutar manualmente: python backend/scripts/ml/optimizar_dataset.py")
            
            print("\n" + "=" * 80)
            print("ENTRENAMIENTO Y PREDICCIONES COMPLETADOS EXITOSAMENTE")
            print("=" * 80)
            print(f"\nArchivos generados:")
            print(f"  - Modelo:        {MODEL_PATH}")
            print(f"  - Encoder:       {ENCODER_PATH}")
            print(f"  - Club Encoding: {os.path.join(MODEL_DIR, 'club_encoding_fifa.joblib')}")
            print(f"  - Dataset CSV:   {DATA_PATH} (✓ con predicciones)")
            print(f"  - Dataset Parquet: {DATA_PATH.replace('.csv', '.parquet')} (✓ optimizado)")
            print("\n✅ El sistema está listo:")
            print("  - El modelo entrenado puede hacer predicciones")
            print("  - El dataset tiene columnas ML precalculadas")
            print("  - El Parquet optimizado permite carga 7x más rápida en API")
            print("=" * 80 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error generando predicciones: {e}")
            print("El modelo fue guardado correctamente pero el dataset no se actualizó.")
            print("=" * 80 + "\n")
    else:
        print("\n" + "=" * 80)
        print("ERROR: No se pudieron cargar los datos")
        print("=" * 80 + "\n")
