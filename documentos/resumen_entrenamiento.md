# RESUMEN DE ENTRENAMIENTO - SISTEMA SCOUTING FIFA

**Fecha**: 8 de noviembre de 2025  
**Dataset**: FIFA 15-21 (122,501 jugadores)  
**Archivo Principal**: `backend/entrenamiento.py`

---

## 1. DATOS DE ENTRADA

**Dataset procesado**: `datos/fifa_limpio.csv`
- **Total registros**: 122,501 jugadores
- **Total columnas**: 69 características
- **Variable objetivo**: `valor_mercado_eur` (transformada con log1p)

**Características seleccionadas para ML**: 14 features
- **11 Numéricas**: valoracion_global, potencial, edad, movimiento_reacciones, regate, tiros, pases, defensa, fisico, pie_habil_rating, movimientos_habilidad
- **3 Categóricas**: posicion_jugador, nacionalidad, pie_preferido

---

## 2. PREPROCESAMIENTO

**Transformación del target**:
```python
y = np.log1p(df['valor_mercado_eur'])
```
- **Razón**: La distribución del valor de mercado es altamente asimétrica (CV=2.39)
- **Efecto**: Reduce el sesgo y mejora la estabilidad del modelo

**Encoding de categóricas**:
```python
OneHotEncoder(sparse_output=False, handle_unknown='ignore')
```
- **posicion_jugador**: 27 posiciones únicas → 27 columnas binarias
- **nacionalidad**: Variable con muchas categorías (162 países)
- **pie_preferido**: Left, Right → 2 columnas binarias

**Resultado final**:
- **Features totales**: 20 columnas (11 numéricas + 9 generadas por encoding)
- **Shape X**: (122501, 20)
- **Shape y**: (122501,)

---

## 3. DIVISIÓN DE DATOS

**Estrategia**: Train/Test split
- **Porcentaje**: 75% entrenamiento, 25% prueba
- **Random state**: 42 (reproducibilidad)

**Resultado**:
- **X_train**: 91,875 filas (75%)
- **X_test**: 30,626 filas (25%)
- **y_train**: 91,875 valores
- **y_test**: 30,626 valores

---

## 4. MODELOS ENTRENADOS

### 4.1 Regresión Lineal (Baseline)

**Configuración**:
```python
LinearRegression()
```

**Resultados**:
- **RMSE**: 1.6631
- **MAE**: 0.5023
- **R²**: 0.4082 (40.82% de varianza explicada)

**Análisis**: Modelo simple que captura relaciones lineales básicas.

---

### 4.2 Random Forest Regressor (MEJOR MODELO)

**Configuración**:
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
```

**Resultados**:
- **RMSE**: 1.5769 (MEJOR)
- **MAE**: 0.4464 (MEJOR)
- **R²**: 0.4680 (MEJOR - 46.80% de varianza explicada)

**Análisis**: Supera a la regresión lineal en todas las métricas. Captura relaciones no lineales entre atributos y valor de mercado. Seleccionado como modelo final según requisitos del proyecto.

---

## 5. COMPARACIÓN DE MODELOS

| Modelo | RMSE | MAE | R² | Ranking |
|--------|------|-----|-----|---------|
| Regresión Lineal (baseline) | 1.6631 | 0.5023 | 0.4082 | 2º |
| **Random Forest** | **1.5769** | **0.4464** | **0.4680** | **1º** |

**Mejora respecto al baseline**:
- RMSE: -5.18% (menor error)
- MAE: -11.13% (menor error absoluto)
- R²: +14.65% (mayor capacidad explicativa)

**Modelos entrenados según requisitos del proyecto**:
- Regresión Lineal: Modelo baseline
- Random Forest Regressor: Modelo principal (seleccionado)

---

## 6. INTERPRETACIÓN DEL MODELO FINAL

**R² = 0.4680**:
- El modelo explica **46.80%** de la variabilidad del valor de mercado
- El 53.20% restante se debe a factores no capturados (reputación del club, contratos, marketing, etc.)

**RMSE = 1.5769**:
- En escala log, el error medio es ~1.58
- En escala original: `exp(1.5769) ≈ 4.84`, es decir, el modelo tiene un error promedio de 4.84x el valor real
- Esto indica que el modelo tiene cierta imprecisión, pero capta patrones generales

**MAE = 0.4464**:
- Error absoluto promedio de 0.45 en escala log
- En escala original: `exp(0.4464) ≈ 1.56`, es decir, error promedio de 56%

---

## 7. ARCHIVOS GENERADOS

**Modelo entrenado**:
```
backend/models/modelo_fifa.joblib
```
- Contiene el modelo LightGBM entrenado
- Tamaño: ~8-10 MB aproximadamente
- Puede ser cargado con: `joblib.load('modelo_fifa.joblib')`

**Encoder de características**:
```
backend/models/encoder_fifa.joblib
```
- Contiene el OneHotEncoder entrenado
- Necesario para transformar nuevas entradas antes de predecir
- Tamaño: ~500 KB aproximadamente

---

## 8. USO DEL MODELO

**Cargar modelo y encoder**:
```python
import joblib
import numpy as np

modelo = joblib.load('backend/models/modelo_fifa.joblib')
encoder = joblib.load('backend/models/encoder_fifa.joblib')
```

**Preparar nuevos datos**:
```python
import pandas as pd

nuevo_jugador = pd.DataFrame({
    'valoracion_global': [85],
    'potencial': [90],
    'edad': [23],
    'movimiento_reacciones': [82],
    'regate': [88],
    'tiros': [78],
    'pases': [80],
    'defensa': [35],
    'fisico': [75],
    'pie_habil_rating': [4],
    'movimientos_habilidad': [4],
    'posicion_jugador': ['ST'],
    'nacionalidad': ['Argentina'],
    'pie_preferido': ['Left']
})

X_nuevo = encoder.transform(nuevo_jugador)
```

**Realizar predicción**:
```python
valor_log_predicho = modelo.predict(X_nuevo)
valor_real_predicho = np.expm1(valor_log_predicho)

print(f"Valor de mercado predicho: €{valor_real_predicho[0]:,.0f}")
```

---

## 9. PRÓXIMOS PASOS

1. **Optimización de hiperparámetros**:
   - GridSearchCV o RandomizedSearchCV para LightGBM
   - Objetivo: Mejorar R² > 0.50

2. **Análisis de importancia de características**:
   - Identificar las 10 features más influyentes
   - Simplificar el modelo eliminando features poco importantes

3. **API REST (FastAPI)**:
   - Endpoint `/ml/predecir` para predicciones en tiempo real
   - Endpoint `/jugadores/buscar` para filtrado avanzado

4. **Dashboard (Streamlit)**:
   - Tab "Predictor de Valor" con sliders interactivos
   - Tab "Jugadores Infravalorados" comparando valor real vs predicho

---

## 10. CONCLUSIONES

El modelo Random Forest Regressor entrenado logra explicar aproximadamente **el 46.80%** de la variabilidad del valor de mercado de los jugadores de fútbol basándose en 14 características técnicas y demográficas.

Si bien este rendimiento es moderado, el modelo es útil para:
- Identificar jugadores infravalorados (valor predicho > valor real)
- Comparar jugadores con perfiles similares
- Estimar rangos de valor de mercado para fichajes

El error RMSE de 1.58 en escala log es razonable dado que el valor de mercado de jugadores depende de múltiples factores cualitativos no medibles (popularidad, contratos, agentes, etc.).

**Modelos implementados según requisitos**:
- Regresión Lineal (baseline): R²=0.4082
- Random Forest Regressor (seleccionado): R²=0.4680

El sistema está listo para pasar a la fase de **exposición mediante API** y **visualización mediante Dashboard**.
