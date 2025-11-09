import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score


def entrenar_regresion_lineal(X_train, X_test, y_train, y_test):
    """
    entrena y evalúa Regresión Lineal (modelo baseline)
    Configuración optimizada para mejor ajuste
    """
    print("\nEntrenando Regresión Lineal (baseline optimizado)...")
    modelo_lr = LinearRegression(
        fit_intercept=True,      # Calcular intercepto
        copy_X=True,             # Copiar datos para preservar originales
        n_jobs=-1,               # Usar todos los núcleos CPU
        positive=False           # Permitir coeficientes negativos
    )
    modelo_lr.fit(X_train, y_train)
    predicciones_lr = modelo_lr.predict(X_test)
    
    rmse_lr = root_mean_squared_error(y_test, predicciones_lr)
    mae_lr = mean_absolute_error(y_test, predicciones_lr)
    r2_lr = r2_score(y_test, predicciones_lr)
    
    print(f"RMSE (Regresión Lineal): {rmse_lr:.4f}")
    print(f"MAE (Regresión Lineal): {mae_lr:.4f}")
    print(f"R² (Regresión Lineal): {r2_lr:.4f}")
    
    return modelo_lr


def entrenar_random_forest(X_train, X_test, y_train, y_test):
    """
    entrena y evalúa Random Forest Regressor (modelo principal)
    CONFIGURACIÓN OPTIMIZADA BASADA EN EDA REAL:
    - Dataset: 122,501 jugadores × ~84 features
    - Hiperparámetros ajustados para máxima precisión
    - R² esperado: 0.65-0.75 (mejora de +10-20 puntos vs modelo anterior)
    """
    RANDOM_STATE = 42
    
    print("\n" + "=" * 70)
    print("ENTRENANDO RANDOM FOREST REGRESSOR - CONFIGURACIÓN OPTIMIZADA")
    print("=" * 70)
    print(f"Dataset: {X_train.shape[0]:,} muestras × {X_train.shape[1]} features")
    print("Hiperparámetros: 4000 estimadores, max_depth=30, min_samples_split=10")
    print("Tiempo estimado: 10-15 minutos con todos los cores CPU")
    print("=" * 70)
    
    modelo_rf = RandomForestRegressor(
        n_estimators=4000,        # 4000 árboles (estabilidad con 84 features)
        max_depth=30,             # Profundidad 30 (captura interacciones club×liga×reputación)
        min_samples_split=10,     # Splits granulares (distingue 954 clubes)
        min_samples_leaf=4,       # Balance: evita overfitting pero permite especificidad
        max_features='sqrt',      # sqrt(84) ≈ 9 features por split (óptimo)
        min_weight_fraction_leaf=0.0,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=True,           # Bootstrap para robustez
        oob_score=True,          #  Validación out-of-bag (sin necesidad de CV)
        criterion='squared_error',
        max_samples=None,
        ccp_alpha=0.0,
        random_state=RANDOM_STATE,
        n_jobs=-1,               # Paralelización total (todos los cores)
        verbose=1,               # Progreso detallado
        warm_start=False
    )
    
    print("\nIniciando entrenamiento...")
    modelo_rf.fit(X_train, y_train)
    
    print("\n✓ Entrenamiento completado")
    
    # Validación OOB (Out-of-Bag)
    if hasattr(modelo_rf, 'oob_score_'):
        print(f"\n  OOB Score (validación interna): {modelo_rf.oob_score_:.4f}")
        print(f"  (Validación usando muestras no vistas en cada árbol)")
    
    # Predicciones en test set
    print("\nRealizando predicciones en test set...")
    predicciones_rf = modelo_rf.predict(X_test)
    
    # Métricas
    rmse_rf = root_mean_squared_error(y_test, predicciones_rf)
    mae_rf = mean_absolute_error(y_test, predicciones_rf)
    r2_rf = r2_score(y_test, predicciones_rf)
    
    print("\n" + "=" * 70)
    print("RESULTADOS RANDOM FOREST:")
    print("=" * 70)
    print(f"RMSE (escala log): {rmse_rf:.4f}")
    print(f"MAE (escala log):  {mae_rf:.4f}")
    print(f"R² (Test):         {r2_rf:.4f} ({r2_rf*100:.2f}%)")
    
    # Comparación OOB vs Test
    if hasattr(modelo_rf, 'oob_score_'):
        diferencia_oob_test = abs(modelo_rf.oob_score_ - r2_rf)
        print(f"\nDiferencia OOB-Test: {diferencia_oob_test:.4f}", end="")
        if diferencia_oob_test < 0.03:
            print(" ✓ (Modelo robusto)")
        else:
            print(" ⚠️ (Posible overfitting)")
    
    print("=" * 70)
    
    return modelo_rf


def entrenar_y_evaluar_modelos(X_train, X_test, y_train, y_test):
    """
    entrena los modelos de regresión solicitados y retorna el mejor según R²
    Modelos: Regresión Lineal (baseline) y Random Forest (principal)
    """
    print("\n---ENTRENANDO MODELOS DE REGRESIÓN---")
    
    # Modelo 1: Regresión Lineal (baseline)
    modelo_lr = entrenar_regresion_lineal(X_train, X_test, y_train, y_test)
    r2_lr = r2_score(y_test, modelo_lr.predict(X_test))
    
    # Modelo 2: Random Forest (principal según requisitos)
    modelo_rf = entrenar_random_forest(X_train, X_test, y_train, y_test)
    r2_rf = r2_score(y_test, modelo_rf.predict(X_test))
    
    # Seleccionar mejor modelo
    if r2_rf >= r2_lr:
        mejor_modelo = modelo_rf
        mejor_nombre = "Random_Forest"
        mejor_r2 = r2_rf
    else:
        mejor_modelo = modelo_lr
        mejor_nombre = "Regresion_Lineal"
        mejor_r2 = r2_lr
    
    print(f"\n---MEJOR MODELO: {mejor_nombre} (R²={mejor_r2:.4f})---")
    
    # Evaluar calidad del modelo
    evaluar_calidad_modelo(mejor_modelo, X_test, y_test, mejor_nombre)
    
    return mejor_modelo


def evaluar_calidad_modelo(modelo, X_test, y_test, nombre_modelo):
    """
    evalúa e interpreta qué tan bueno es el modelo entrenado
    """
    print("\n" + "=" * 70)
    print("EVALUACIÓN DE CALIDAD DEL MODELO")
    print("=" * 70)
    
    y_pred = modelo.predict(X_test)
    
    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModelo seleccionado: {nombre_modelo}")
    print(f"\nMétricas de evaluación:")
    print(f"  - R² (Coeficiente de determinación): {r2:.4f}")
    print(f"  - RMSE (Error cuadrático medio): {rmse:.4f}")
    print(f"  - MAE (Error absoluto medio): {mae:.4f}")
    
    # Interpretación de R²
    print(f"\nInterpretación de R²:")
    porcentaje_explicado = r2 * 100
    porcentaje_no_explicado = (1 - r2) * 100
    print(f"  - El modelo explica {porcentaje_explicado:.2f}% de la variabilidad del valor de mercado")
    print(f"  - El {porcentaje_no_explicado:.2f}% restante se debe a factores no capturados")
    
    # Interpretación actualizada basada en expectativas realistas
    if r2 >= 0.75:
        calificacion = "EXCELENTE"
        comentario = "Supera el objetivo del proyecto (R² > 0.75)"
    elif r2 >= 0.65:
        calificacion = "MUY BUENO"
        comentario = "Dentro del rango esperado con nuevas features (0.65-0.75)"
    elif r2 >= 0.55:
        calificacion = "BUENO"
        comentario = "Mejora sobre modelo anterior (0.5495) pero con margen de optimización"
    elif r2 >= 0.40:
        calificacion = "MODERADO"
        comentario = "Rendimiento similar a baseline, requiere ajustes"
    else:
        calificacion = "BAJO"
        comentario = "Bajo rendimiento, revisar preprocesamiento"
    
    print(f"\nCalificación del modelo: {calificacion}")
    print(f"  → {comentario}")
    
    # Interpretación de errores en escala original
    print(f"\nErrores en escala original (valor de mercado EUR):")
    
    # Como aplicamos log1p, debemos revertirlo
    y_test_original = np.expm1(y_test)
    y_pred_original = np.expm1(y_pred)
    
    error_absoluto_promedio = np.mean(np.abs(y_test_original - y_pred_original))
    
    # Calcular error relativo evitando divisiones por cero
    errores_relativos = []
    for real, pred in zip(y_test_original, y_pred_original):
        if isinstance(real, (int, float)):
            real_val = real
        else:
            real_val = real if not hasattr(real, 'iloc') else real
        
        if real_val > 0:
            error_rel = abs((pred - real_val) / real_val) * 100
            errores_relativos.append(error_rel)
    
    error_relativo_promedio = np.mean(errores_relativos) if errores_relativos else 0
    
    print(f"  - Error absoluto promedio: €{error_absoluto_promedio:,.0f}")
    print(f"  - Error relativo promedio: {error_relativo_promedio:.1f}%")
    
    # Ejemplos de predicciones
    print(f"\nEjemplos de predicciones (primeros 5 jugadores del test):")
    print(f"{'Real':>15} {'Predicho':>15} {'Diferencia':>15} {'Error %':>10}")
    print("-" * 60)
    
    for i in range(min(5, len(y_test))):
        real = y_test_original.iloc[i] if hasattr(y_test_original, 'iloc') else y_test_original[i]
        pred = y_pred_original[i]
        diff = pred - real
        error_pct = abs(diff / real * 100) if real != 0 else 0
        
        print(f"€{real:>13,.0f} €{pred:>13,.0f} €{diff:>13,.0f} {error_pct:>9.1f}%")
    
    print("\n" + "=" * 70)
