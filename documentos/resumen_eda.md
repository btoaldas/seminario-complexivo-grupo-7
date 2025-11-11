# RESUMEN EJECUTIVO - ANÁLISIS EXPLORATORIO DE DATOS (EDA)
## Sistema de Scouting y Valoración de Jugadores de Fútbol

**Fecha:** 8 de noviembre de 2025  
**Dataset:** FIFA 15-21 (122,501 jugadores, 69 columnas)  
**Notebook:** `notebooks/eda_fifa_scouting.ipynb`

---

## 1. OBJETIVO DEL ANÁLISIS

Descubrir qué atributos se correlacionan más con el **valor de mercado** de un jugador profesional de fútbol, con el fin de construir un modelo predictivo de Machine Learning.

---

## 2. DATASET ANALIZADO

### Características Generales:
- **Total de jugadores:** 122,501
- **Columnas totales:** 69 (64 originales + 5 features ingenieradas)
- **Versiones FIFA incluidas:** 2015, 2016, 2017, 2018, 2019, 2020, 2021
- **Memoria utilizada:** 154.16 MB
- **Calidad de datos:** 0 valores nulos (100% completo tras limpieza)

### Variable Objetivo: `valor_mercado_eur`
- **Media:** €2,050,152
- **Mediana:** €600,000
- **Desviación estándar:** €4,891,098
- **Rango:** €0 - €123,000,000
- **Coeficiente de variación:** 2.39 (distribución muy dispersa)

**Observación crítica:** La distribución está altamente sesgada a la derecha, lo que indica que la mayoría de jugadores tienen valores bajos, pero unos pocos tienen valores extremadamente altos.

---

## 3. HALLAZGOS PRINCIPALES

### 3.1 TOP 20 ATRIBUTOS MÁS CORRELACIONADOS CON VALOR DE MERCADO

| Posición | Atributo                  | Correlación | Categoría          |
|----------|---------------------------|-------------|--------------------|
| 1        | clausula_rescision_eur    | 0.8359      | Financiero (excluir)|
| 2        | salario_eur               | 0.8231      | Financiero (excluir)|
| 3        | **valoracion_global**     | **0.6067**  | **Predictor principal** |
| 4        | **potencial**             | **0.5631**  | **Predictor principal** |
| 5        | movimiento_reacciones     | 0.5178      | Técnico            |
| 6        | calidad_promedio          | 0.4560      | Ingenierada        |
| 7        | pase                      | 0.3983      | Técnico            |
| 8        | mentalidad_compostura     | 0.3856      | Mental             |
| 9        | regate_gambeta            | 0.3849      | Técnico            |
| 10       | mentalidad_vision         | 0.3341      | Mental             |
| 11       | tiro_disparo              | 0.3129      | Técnico            |
| 12       | ataque_pase_corto         | 0.3086      | Técnico            |
| 13       | habilidad_control_balon   | 0.2897      | Técnico            |
| 14       | habilidad_pase_largo      | 0.2870      | Técnico            |
| 15       | potencia_disparo          | 0.2799      | Físico             |
| 16       | habilidad_efecto          | 0.2717      | Técnico            |
| 17       | ataque_voleas             | 0.2682      | Técnico            |
| 18       | habilidades_regate        | 0.2624      | Técnico            |
| 19       | potencia_tiros_lejanos    | 0.2604      | Físico             |
| 20       | habilidad_regate          | 0.2554      | Técnico            |

**Nota importante:** `clausula_rescision_eur` y `salario_eur` deben **excluirse** del modelo porque causan **data leakage** (están derivados del valor de mercado).

### 3.2 Relación Valoración Global vs Valor de Mercado

- **Correlación de Pearson:** 0.6067 (correlación positiva fuerte)
- **Interpretación:** A mayor valoración global, mayor valor de mercado
- **Relación:** No perfectamente lineal, jugadores con valoración > 85 tienen valores exponencialmente mayores

### 3.3 Relación Potencial vs Valor de Mercado

- **Correlación de Pearson:** 0.5631 (correlación positiva moderada-fuerte)
- **Interpretación:** Jugadores jóvenes con alto potencial (>80) representan oportunidades de inversión

### 3.4 Efecto de Variables Categóricas

#### Por Categoría de Edad:
- **Prime (24-31 años):** Valores promedio más altos
- **Jóvenes (<24 años):** Alto potencial de crecimiento, valores moderados
- **Veteranos (>31 años):** Valores significativamente menores

#### Por Categoría de Posición:
- **Atacantes:** Valores promedio más altos
- **Mediocampistas:** Valores intermedios-altos
- **Defensas:** Valores intermedios
- **Porteros:** Distribución diferente, menor correlación con atributos ofensivos

### 3.5 Features Ingenieradas Exitosas

1. **calidad_promedio** (correlación 0.4560)
   - Promedio de: pase, regate, tiro, defensa, físico, velocidad
   - Resume eficientemente el rendimiento técnico general
   
2. **diferencia_potencial**
   - Fórmula: potencial - valoracion_global
   - Identifica jugadores con margen de crecimiento
   
3. **ratio_valor_salario**
   - Fórmula normalizada: valor_mercado_eur / (salario_eur × 52)
   - Identifica jugadores infravalorados/sobrevalorados

---

## 4. CONCLUSIONES ESTRATÉGICAS

### 4.1 Para el Modelo de Machine Learning:

1. **Los mejores predictores son:**
   - valoracion_global (0.6067)
   - potencial (0.5631)
   - movimiento_reacciones (0.5178)
   - calidad_promedio (0.4560)

2. **Atributos técnicos específicos tienen relevancia moderada:**
   - Pase, compostura, regate, visión (0.30-0.40)

3. **La edad y posición del jugador impactan significativamente**

4. **Transformación logarítmica necesaria:**
   - La distribución del valor está muy sesgada
   - Se debe aplicar log1p() a la variable objetivo

### 4.2 Para Scouts y Analistas:

1. **Jugadores infravalorados:**
   - Jóvenes (<23 años) con potencial ≥80 y diferencia_potencial ≥5
   - Valoración global baja pero atributos técnicos específicos altos

2. **Factores clave de valoración:**
   - Reacciones, compostura y visión son críticos
   - No solo importa el overall, sino atributos mentales específicos

3. **Oportunidades de mercado:**
   - Jugadores con ratio_valor_salario bajo
   - Alto potencial pero valoración actual moderada

---

## 5. PREPARACIÓN PARA FASE DE ML

### 5.1 Features Seleccionadas (14 Total)

#### Features Numéricas (11):
1. valoracion_global (correlación: 0.6067)
2. potencial (correlación: 0.5631)
3. movimiento_reacciones (correlación: 0.5178)
4. calidad_promedio (correlación: 0.4560)
5. pase (correlación: 0.3983)
6. mentalidad_compostura (correlación: 0.3856)
7. regate_gambeta (correlación: 0.3849)
8. mentalidad_vision (correlación: 0.3341)
9. tiro_disparo (correlación: 0.3129)
10. ataque_pase_corto (correlación: 0.3086)
11. edad (correlación: 0.0866)

#### Features Categóricas (3):
1. categoria_posicion (4 categorías únicas)
2. categoria_edad (3 categorías únicas)
3. pie_preferido (2 categorías únicas)

### 5.2 División del Dataset

- **Train set (75%):** ~91,875 jugadores
- **Test set (25%):** ~30,625 jugadores
- **Validación cruzada:** 5-fold CV

### 5.3 Preprocesamiento Necesario

**Transformaciones:**
1. **Variable objetivo:** Aplicar `np.log1p(valor_mercado_eur)`
2. **Features numéricas:** Aplicar `StandardScaler()`
3. **Features categóricas:** Aplicar `OneHotEncoder()`

**Pipeline sugerido:**
```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), features_numericas),
        ('cat', OneHotEncoder(drop='first'), features_categoricas)
    ])
```

### 5.4 Modelos a Entrenar

#### Modelo 1: Regresión Lineal (Baseline)
- **Objetivo:** Establecer línea base
- **R² esperado:** 0.45-0.55
- **Ventajas:** Simple, interpretable, rápido

#### Modelo 2: Random Forest Regressor (Principal)
- **Objetivo:** Modelo principal del sistema
- **R² esperado:** 0.65-0.80
- **Ventajas:** Maneja no linealidad, robusto, feature importance

#### Modelo 3: Gradient Boosting (Optimizado)
- **Objetivo:** Máxima precisión
- **R² esperado:** >0.80
- **Opciones:** LightGBM, XGBoost

### 5.5 Métricas de Evaluación

**Métricas principales:**
- **R² (R-squared):** Objetivo > 0.75
- **RMSE:** Objetivo < €3,000,000
- **MAE:** Objetivo < €1,500,000
- **MAPE:** Para error porcentual

**Validación adicional:**
- Análisis de residuales
- Feature importance
- Cross-validation 5-fold

---

## 6. PRÓXIMOS PASOS

### Fase ML (Siguiente):

1. **Crear script de entrenamiento**
   - Archivo: `backend/entrenamiento_modelo_ml.py`
   - Implementar pipeline completo

2. **Entrenar y evaluar modelos**
   - Comparar Regresión Lineal, Random Forest, Gradient Boosting
   - Validación cruzada

3. **Optimizar hiperparámetros**
   - GridSearchCV o RandomizedSearchCV
   - Seleccionar mejor modelo

4. **Persistir modelo entrenado**
   - Guardar en `backend/models/modelo_fifa.joblib`
   - Guardar encoder en `backend/models/encoder_fifa.joblib`

5. **Documentar resultados**
   - Métricas finales
   - Feature importance
   - Casos de uso

---

## 7. ANEXOS

### A. Archivos Generados

- **Notebook EDA:** `notebooks/eda_fifa_scouting.ipynb`
- **Dataset limpio:** `datos/fifa_limpio.csv` (48.89 MB)
- **Dataset Excel:** `datos/fifa_limpio.xlsx`
- **Este resumen:** `documentacion/resumen_eda.md`

### B. Comandos para Ejecutar Notebook

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Iniciar Jupyter
jupyter notebook notebooks/eda_fifa_scouting.ipynb
```

### C. Librerías Utilizadas

- pandas 2.x
- numpy 2.x
- matplotlib 3.x
- seaborn 0.x
- openpyxl (para Excel)

---

**ANÁLISIS EDA COMPLETADO EXITOSAMENTE**  
**SISTEMA LISTO PARA FASE DE ENTRENAMIENTO ML**
