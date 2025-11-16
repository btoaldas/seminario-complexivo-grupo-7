# 📊 Análisis Exploratorio de Datos (EDA) - FIFA Scouting System

Este directorio contiene el análisis exploratorio completo del dataset FIFA utilizado para construir el modelo de Machine Learning de predicción de valores de mercado.

---

## 📁 Contenido del Directorio

### `eda_fifa_scouting.ipynb`
Notebook Jupyter con el análisis exploratorio completo del dataset FIFA 15-21.

**Contenido del notebook:**
- ✅ Carga y exploración inicial del dataset (122,501 jugadores × 73 columnas)
- ✅ Análisis de la variable objetivo (`valor_mercado_eur`)
- ✅ Matriz de correlación completa (73 variables numéricas)
- ✅ Identificación del Top 20 de predictores más correlacionados
- ✅ Análisis univariado por feature crítica (overall, potencial, posición, edad)
- ✅ Análisis de nuevas features contextuales (club, liga, reputación internacional)
- ✅ Análisis cruzado multivariado (Liga × Reputación × Valor)
- ✅ Detección de jugadores "promesa" (alto potencial infravalorados)
- ✅ Recomendaciones finales para configuración de Random Forest

---

## 🎯 Objetivo del Análisis

**Descubrir qué atributos de los jugadores de fútbol se correlacionan más fuertemente con su valor de mercado**, para construir un modelo de Machine Learning capaz de:

1. **Predecir valores justos** de jugadores basándose en sus características técnicas y contextuales
2. **Detectar oportunidades de mercado** (jugadores infravalorados con alto potencial)
3. **Prevenir sobrepagos** (jugadores sobrevalorados por factores no técnicos)
4. **Objetivizar el proceso de scouting** mediante datos y estadística

---

## 📊 Dataset Analizado

### Características Generales
- **Fuente:** Base de datos FIFA 15-21 (videojuego)
- **Tamaño:** 122,501 jugadores únicos
- **Columnas:** 73 variables (atributos técnicos, demográficos y contextuales)
- **Variable objetivo:** `valor_mercado_eur` (valor de mercado en euros)
- **Calidad:** 0 valores nulos después del proceso de limpieza
- **Versiones FIFA incluidas:** 7 versiones (2015, 2016, 2017, 2018, 2019, 2020, 2021)

### Estadísticas del Valor de Mercado
- **Media:** €2,050,152
- **Mediana:** €600,000
- **Desviación estándar:** €4,909,346
- **Coeficiente de variación (CV):** 2.39 (alta dispersión)
- **Rango:** €0 - €123,000,000 (Neymar)
- **Distribución:** Altamente sesgada a la derecha (requiere transformación logarítmica)

---

## 🔍 Hallazgos Principales

### Top 10 Predictores del Valor de Mercado

| Ranking | Atributo | Correlación | Fuerza | Uso en Modelo |
|---------|----------|-------------|--------|---------------|
| 1 | **salario_eur** | 0.8231 | MUY FUERTE | ❌ Data Leakage - NO USAR |
| 2 | **reputacion_internacional** | 0.6423 | FUERTE | ✅ Mejor predictor válido |
| 3 | **valoracion_global** | 0.6067 | FUERTE | ✅ Predictor principal |
| 4 | **potencial** | 0.5631 | FUERTE | ✅ Predictor secundario |
| 5 | **movimiento_reacciones** | 0.5178 | FUERTE | ✅ Atributo técnico top |
| 6 | **calidad_promedio** | 0.4560 | MODERADA | ✅ Feature ingenierada |
| 7 | **pase** | 0.3983 | MODERADA | ✅ Habilidad técnica |
| 8 | **mentalidad_compostura** | 0.3856 | MODERADA | ✅ Atributo mental |
| 9 | **regate_gambeta** | 0.3849 | MODERADA | ✅ Habilidad ofensiva |
| 10 | **mentalidad_vision** | 0.3341 | MODERADA | ✅ Atributo táctico |

### Impacto de Variables Contextuales

#### 🏟️ Club (954 clubes únicos)
- Bayern München: **€24.23M** promedio
- FC Barcelona: **€23.79M** promedio
- Real Madrid: **€23.47M** promedio
- **Diferencia:** Clubes élite valen **15-20x más** que el promedio (€2M)
- **Encoding:** Target Encoding → `club_valor_promedio`

#### 🏆 Liga (56 ligas únicas)
- English Premier League: **€8.10M** (n=4,532)
- Spain Primera Division: **€7.77M** (n=4,266)
- German 1. Bundesliga: **€6.47M** (n=3,784)
- **Diferencia:** Ligas top valen **4-8x más** que ligas bajas
- **Encoding:** OneHot Encoding (56 columnas)

#### ⭐ Reputación Internacional (1-5)
- Nivel 5 (Mundial): **€65.89M** (n=47)
- Nivel 4 (Continental): **€35.97M** (n=327)
- Nivel 3 (Nacional): **€18.53M** (n=1,927)
- Nivel 2 (Regional): **€6.75M** (n=8,802)
- Nivel 1 (Local): **€1.27M** (n=111,398)
- **Diferencia:** Nivel 5 vale **52x más** que nivel 1
- **Correlación:** 0.6423 (segundo mejor predictor)

---

## 🧠 Decisiones para el Modelo de Machine Learning

### Features Seleccionadas

#### Features Numéricas (14 features)
**Correlación FUERTE (> 0.50):**
- reputacion_internacional (0.6423)
- valoracion_global (0.6067)
- potencial (0.5631)
- movimiento_reacciones (0.5178)

**Correlación MODERADA (0.30 - 0.50):**
- calidad_promedio, pase, mentalidad_compostura, regate_gambeta, mentalidad_vision, tiro_disparo, ataque_pase_corto

**Correlación DÉBIL pero ÚTILES:**
- anos_contrato_restantes (0.1267)
- ratio_valor_salario (0.1199) - previene data leakage
- club_valor_promedio (Target Encoding)

#### Features Categóricas (5 features → 70 columnas)
- categoria_posicion (4 categorías)
- categoria_edad (3 categorías)
- pie_preferido (2 categorías)
- liga (56 categorías) - OneHot
- categoria_reputacion (5 categorías) - OneHot

**Total features finales:** ~84 (14 numéricas + 70 categóricas)

---

### Configuración Optimizada de Random Forest

```python
RandomForestRegressor(
    n_estimators=2000,          # Aumentado para estabilidad con 84 features
    max_depth=30,               # Árboles profundos para interacciones club/liga
    min_samples_split=10,       # Granularidad para 954 clubes
    min_samples_leaf=4,         # Prevenir overfitting
    max_features='sqrt',        # sqrt(84) ≈ 9 features por split
    bootstrap=True,
    oob_score=True,             # Validación out-of-bag gratuita
    n_jobs=-1,
    random_state=42
)
```

### Preprocesamiento Aplicado

#### 1. Transformación de Variable Objetivo
```python
# Transformación logarítmica (normaliza distribución CV=2.39)
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)

# Reversión en predicciones
predicciones_eur = np.expm1(modelo.predict(X_test))
```

#### 2. Target Encoding para Club
```python
# Club: 954 categorías → 1 columna numérica
club_encoding = df.groupby('club')['valor_mercado_eur'].mean()
df['club_valor_promedio'] = df['club'].map(club_encoding)
df['club_valor_promedio'].fillna(df['valor_mercado_eur'].median(), inplace=True)
```

#### 3. OneHot Encoding para Categóricas
```python
X_encoded = pd.get_dummies(X, columns=[
    'liga', 
    'categoria_posicion', 
    'categoria_edad', 
    'pie_preferido',
    'categoria_reputacion'
], drop_first=True)
```

#### 4. NO Aplicar Escalamiento
❌ **NO usar StandardScaler/MinMaxScaler**
- Random Forest es invariante a escalamiento
- Mantener valores originales mejora interpretabilidad

---

## 📈 Resultados Esperados

### Métricas de Evaluación

| Métrica | Modelo Anterior | Modelo con EDA | Mejora Esperada |
|---------|-----------------|----------------|-----------------|
| **R²** | 0.5495 (54.95%) | 0.65-0.75 | **+10-20 puntos** |
| **RMSE** | 1.4512 (log) | 1.15-1.25 (log) | **-20% error** |
| **Features** | 48 | 84 | **+75% información** |

### ¿Por Qué Esta Mejora?

1. **Club** captura "brand premium" que atributos técnicos no reflejan
2. **Liga** captura poder adquisitivo del mercado regional
3. **Reputación** captura estatus global del jugador
4. Estas 3 features contextuales explican **~15-25% de varianza adicional**

---

## 📊 Visualizaciones Generadas

El notebook incluye las siguientes visualizaciones clave:

1. **Matriz de Correlación (Heatmap)** - Top 15 atributos más correlacionados
2. **Distribución del Valor de Mercado** - Histograma + Boxplot
3. **Relación Valoración Global vs Valor** - Scatter plot + tendencia lineal
4. **Relación Potencial vs Valor** - Scatter plot + tendencia lineal
5. **Valor Promedio por Liga** - Barplot horizontal (Top 15 ligas)
6. **Distribución por Reputación Internacional** - Boxplot (niveles 1-5)
7. **Top 20 Jugadores Más Valiosos** - Barplot horizontal
8. **Distribución por Posición** - Boxplot + Promedios
9. **Distribución por Edad** - Boxplot + Promedios
10. **Heatmap Liga × Reputación × Valor** - Análisis cruzado multivariado
11. **Top 20 Jugadores Promesa** - Alto potencial infravalorados
12. **Top 20 Clubes por Valor Promedio** - Boxplot comparativo

---

## 💎 Casos de Uso del Modelo

### 1. Detección de Jugadores Infravalorados
```python
diferencia_porcentual = ((valor_predicho - valor_real) / valor_real) * 100
infravalorado = diferencia_porcentual < -8%
```
**Acción:** Oportunidad de compra (mercado no ha reconocido su valor)

### 2. Detección de Jugadores Sobrevalorados
```python
sobrevalorado = diferencia_porcentual > +8%
```
**Acción:** Evitar compra (precio inflado por factores no técnicos)

### 3. Valoración Justa
```python
justo = abs(diferencia_porcentual) <= 8%
```
**Acción:** Precio de mercado refleja capacidades técnicas

---

## 🚀 Cómo Ejecutar el Notebook

### Prerrequisitos

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Instalar dependencias
pip install pandas numpy matplotlib seaborn jupyter
```

### Ejecución

```bash
# Opción 1: Abrir en Jupyter Notebook
jupyter notebook eda_fifa_scouting.ipynb

# Opción 2: Abrir en VS Code
code eda_fifa_scouting.ipynb
```

### Tiempo de Ejecución
- **Carga de datos:** ~5 segundos
- **Análisis completo:** ~2-3 minutos
- **Generación de visualizaciones:** ~1 minuto
- **Total:** ~5 minutos (con todas las celdas ejecutadas)

---

## 📚 Estructura del Notebook

### Pasos del Análisis

1. **PASO 1:** Importar librerías necesarias
2. **PASO 2:** Cargar dataset limpio (`fifa_limpio.csv`)
3. **PASO 3:** Exploración inicial (dimensiones, tipos, memoria)
4. **PASO 4:** Análisis de variable objetivo (`valor_mercado_eur`)
5. **PASO 5:** Matriz de correlación completa
6. **PASO 6:** Top 20 atributos más correlacionados
7. **PASO 7:** Heatmap de correlación (Top 15)
8. **PASO 8:** Análisis Valoración Global vs Valor
9. **PASO 9:** Análisis Potencial vs Valor
10. **PASO 10:** Análisis por Categoría de Posición
11. **PASO 11:** Análisis por Categoría de Edad
12. **PASO 12:** Top 20 jugadores más valiosos
13. **PASO 13:** Jugadores promesa (alto potencial infravalorados)
14. **PASO 14:** Conclusiones y recomendaciones para ML
15. **PASO 15:** Análisis de nuevas columnas críticas (club, liga, reputación)

---

## ✅ Conclusiones Principales

### Hallazgos Técnicos

1. **Reputación internacional** (0.6423) es el mejor predictor válido
2. **Club y Liga** explican ~15-25% de varianza adicional
3. **Transformación logarítmica** es esencial (CV=2.39)
4. **Features técnicas** capturan capacidades del jugador
5. **Features contextuales** capturan valor de mercado institucional

### Impacto Práctico

1. Sistema identifica oportunidades de compra (jugadores infravalorados)
2. Previene sobrepagos (jugadores sobrevalorados)
3. Objetiviza negociaciones con valores de referencia
4. Acelera scouting filtrando 122,501 jugadores eficientemente

### Robustez del Análisis

- Dataset de alta calidad (0 valores nulos)
- Muestra representativa (122,501 jugadores, 7 versiones FIFA)
- Metodología rigurosa (análisis univariado, bivariado, multivariado)
- Validación estadística confirmada (correlaciones, visualizaciones)

---

## 🎯 Próximos Pasos

### Implementación del Modelo

1. ✅ Actualizar `preprocesamiento_modelo.py` con nuevas features
2. ✅ Implementar Target Encoding para club
3. ✅ Implementar OneHot Encoding para liga y reputación
4. ✅ Entrenar Random Forest con configuración optimizada (2000 árboles, max_depth=30)
5. ✅ Validar mejora de R² (objetivo: 0.65-0.75)
6. ✅ Analizar Feature Importance post-entrenamiento
7. ✅ Guardar modelo en `backend/models/modelo_fifa.joblib`

### Integración con Dashboard

1. ✅ Generar predicciones para 122,501 jugadores
2. ✅ Calcular clasificación ML (💎 infravalorado, ⚠️ sobrevalorado, ✓ justo)
3. ✅ Implementar filtros combinados en Streamlit
4. ✅ Cachear predicciones para performance
5. ✅ Desplegar en producción (Docker)

---

## 📖 Referencias

### Documentación Relacionada

- **Resumen Ejecutivo:** `../documentos/RESUMEN_EDA_EXPOSICION.md` (52 páginas)
- **Dataset Limpio:** `../datos/procesados/fifa_limpio.csv` (122,501 × 73)
- **Dataset Optimizado:** `../datos/procesados/fifa_limpio.parquet` (77% más pequeño)
- **Scripts de Preprocesamiento:** `../scripts/` (data_loader, data_cleaning, etc.)
- **Modelo Entrenado:** `../backend/models/modelo_fifa.joblib`
- **Dashboard:** `../frontend/dashboard_scouting_fifa.py`

### Archivos Generados por el EDA

- `eda_fifa_scouting.ipynb` - Notebook completo ejecutado
- Configuración final de features (14 numéricas + 5 categóricas)
- Recomendaciones para Random Forest (hiperparámetros optimizados)
- Lista de features a excluir (salario_eur, clausula_rescision_eur)

---

## 🏆 Contribuciones

**Autores:**
- Alberto Alexander Aldás Villacrés
- Cristian Joel Riofrío Medina
- Wilson Fernando Saavedra Álvarez

**Institución:** Universidad Regional Autónoma de los Andes (UNIANDES)  
**Carrera:** Ingeniería de Software  
**Asignatura:** Analítica con Python  
**Docente:** Prof. Juan Felipe Nájera  
**Fecha:** Noviembre 2025

---

## 📌 Datos Clave para Recordar

- **122,501 jugadores** × **73 columnas**
- **R² esperado:** 0.65-0.75 (mejora +15% vs modelo base)
- **Top 3 predictores:** Reputación (0.64), Overall (0.61), Potencial (0.56)
- **Impactos contextuales:** Club 15-20x, Liga 4-8x, Reputación 52x
- **Transformación log** es esencial (CV=2.39)
- **84 features finales** (14 numéricas + 70 categóricas)
- **2000 árboles**, profundidad **30**, OOB score activado

---

**FIN DEL README**

*Para más detalles, consultar el resumen ejecutivo completo en `../documentos/RESUMEN_EDA_EXPOSICION.md`*
