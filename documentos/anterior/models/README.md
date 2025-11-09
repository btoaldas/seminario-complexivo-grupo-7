# Modelos de Machine Learning - FIFA Scouting

## ⚠️ Archivos No Incluidos en el Repositorio

Los archivos `.pkl` de los modelos **NO están incluidos** en el repositorio de GitHub porque superan el límite de tamaño (100 MB).

## 📋 Archivos Necesarios

Para que el sistema funcione completamente, necesitas generar estos archivos:

1. **`modelo_valoracion_fifa.pkl`** (≈109 MB)
   - Modelo Random Forest entrenado con 120,679 jugadores
   - Predice el valor de mercado (`valor_euros`)

2. **`encoder_categoricas.pkl`** (≈5 KB)
   - Encoder One-Hot para variables categóricas
   - Convierte posición y pie preferido a números

3. **`columnas_modelo.pkl`** (≈1 KB)
   - Lista de columnas esperadas por el modelo
   - Necesario para procesar datos de entrada

## 🔧 Cómo Generar los Modelos

### Opción 1: Ejecutar el Notebook de ML

1. Abre el notebook: `notebooks/modelo_ml.ipynb`
2. Ejecuta todas las celdas en orden
3. Los archivos `.pkl` se generarán automáticamente en esta carpeta

### Opción 2: Línea de Comandos (próximamente)

```bash
# En el futuro, podrás ejecutar:
python scripts/entrenar_modelo.py
```

## 📊 Información Técnica de los Modelos

### Modelo Random Forest Regressor

**Configuración:**
- Algoritmo: `RandomForestRegressor` (sklearn)
- Número de árboles: 100
- Profundidad máxima: 20
- Random state: 42

**Variables de entrada (9 features):**
- `edad` (numérica)
- `calificacion_general` (numérica) ⭐ Más importante
- `potencial` (numérica)
- `altura_cm` (numérica)
- `peso_kg` (numérica)
- `imc` (numérica)
- `margen_crecimiento` (numérica)
- `posicion_principal` (categórica → One-Hot)
- `pie_preferido` (categórica → One-Hot)

**Variable objetivo:**
- `valor_euros` (valor de mercado en euros)

**Rendimiento esperado:**
- R² Score: > 0.75 (explica +75% de la variabilidad)
- RMSE: ≈ €2-3 millones
- MAE: ≈ €1-2 millones

## 🎯 Uso de los Modelos

Los modelos se cargan en el dashboard de Streamlit para:

1. **Predecir valor de jugadores**: Basándose en características ingresadas
2. **Identificar infravalorados**: Valor real < Valor predicho
3. **Identificar sobrevalorados**: Valor real > Valor predicho

## 📝 Notas Importantes

- Los modelos se entrenan con datos de FIFA 15-21
- La predicción es una **estimación** basada en datos históricos
- Factores no incluidos: marca personal, lesiones, forma actual, etc.
- Se recomienda re-entrenar el modelo con datos actualizados periódicamente

## 🔄 Re-entrenamiento

Para actualizar los modelos con nuevos datos:

1. Actualiza el dataset: `data/processed/fifa_limpio.csv`
2. Ejecuta el notebook de ML nuevamente
3. Los archivos `.pkl` se sobrescribirán automáticamente

---

**Fecha última actualización:** 31 de octubre de 2025
**Versión del modelo:** 1.0
**Dataset utilizado:** FIFA 15-21 (120,679 jugadores)
