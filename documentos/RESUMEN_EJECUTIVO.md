================================================================================
RESUMEN EJECUTIVO - SISTEMA DE SCOUTING FIFA
================================================================================
Fecha: 8 de noviembre de 2025
================================================================================

## 📋 CONTEXTO DEL DATASET FIFA 21

### Datos Principales
- **Total de jugadores**: 16,155
- **Total de columnas**: 106
- **Formato**: Excel (fifa.xlsx)
- **Fuente**: Dataset FIFA 21 de Kaggle

### Columnas Más Importantes
```
✓ short_name, long_name          → Nombres del jugador
✓ age, dob                        → Edad y fecha de nacimiento
✓ height_cm, weight_kg            → Físico
✓ nationality, club_name          → Información demográfica
✓ overall, potential              → Calificación general y potencial
✓ value_eur, wage_eur             → VALOR DE MERCADO (€) y salario
✓ player_positions                → Posición(es) del jugador
✓ pace, shooting, passing         → Atributos técnicos principales
✓ dribbling, defending, physic    → Más atributos técnicos
✓ weak_foot, skill_moves          → Habilidades especiales
✓ work_rate, preferred_foot       → Características de juego
```

### Valores Clave del Dataset
- **Valor promedio**: 1.06 millones EUR
- **Edad promedio**: 24.8 años
- **Overall promedio**: 63.8
- **Potential promedio**: 68.4
- **Jugador más valioso**: 100.5 millones EUR (Messi)

### Retos de Limpieza Identificados
- ❌ `release_clause_eur`: 100% nulos (eliminar)
- ❌ `mentality_composure`: 100% nulos (eliminar)
- ⚠️ Atributos de portero (`gk_*`): 89% nulos (imputar 0 para jugadores de campo)
- ⚠️ `pace, shooting, passing, dribbling, defending, physic`: 11% nulos (imputar mediana por posición)
- ⚠️ `loaned_from`: 94% nulos (OK, es información opcional)

---

## 🎯 OBJETIVO DEL PROYECTO

### Objetivo Principal
Construir un **Sistema de Scouting Inteligente** que prediga el valor de mercado de jugadores de fútbol mediante Machine Learning (regresión) y permita identificar talento infravalorado.

### Variable a Predecir (Target)
**`value_eur`** - Valor de mercado en euros

### Features Principales para el Modelo
1. **Demográficas**: age, nationality, club_name, player_positions
2. **Técnicas**: overall, potential, pace, shooting, passing, dribbling, defending, physic
3. **Especiales**: weak_foot, skill_moves, work_rate, preferred_foot
4. **Derivadas**: calidad_promedio, diferencia_potencial, categoria_edad

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO FINAL                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              STREAMLIT DASHBOARD                             │
│  ┌─────────────┬──────────────┬──────────────┬────────────┐ │
│  │ Búsqueda    │ Análisis EDA │ Predicción ML│ Infravalo. │ │
│  │ Jugadores   │ Mercado      │ Valor        │ -rados     │ │
│  └─────────────┴──────────────┴──────────────┴────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP Requests
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI REST API                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ GET  /jugadores/filtros         → Opciones de filtros  │ │
│  │ GET  /jugadores/buscar          → Búsqueda con filtros │ │
│  │ GET  /jugadores/{id}            → Perfil de jugador    │ │
│  │ POST /ml/predecir               → Predicción de valor  │ │
│  │ GET  /eda/estadisticas          → KPIs generales       │ │
│  │ GET  /eda/datos_graficos        → Datos para gráficos  │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              MODELOS Y DATOS                                 │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • modelo_regresion.joblib  (Random Forest / LightGBM)  │ │
│  │ • encoder.joblib            (OneHotEncoder)            │ │
│  │ • jugadores_limpios.csv     (Dataset procesado)        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 FASES DEL PROYECTO

### FASE 1: PIPELINE DE DATOS (backend/pipeline/)
```python
main.py  →  cargar_datos()
         →  limpieza_datos()
         →  imputacion_datos()
         →  nuevas_caracteristicas()
         →  guardar_datos()
```

**Input**: `datos/crudos/fifa.xlsx` (16,155 × 106)  
**Output**: `datos/procesados/jugadores_limpios.csv` (optimizado)

### FASE 2: ANÁLISIS EXPLORATORIO (backend/eda/)
- Notebooks Jupyter con visualizaciones
- Identificación de correlaciones
- Insights sobre el mercado
- Patrones por posición/edad/nacionalidad

### FASE 3: MACHINE LEARNING (backend/ml/)
```python
entrenar.py  →  preprocesar_datos()
             →  entrenar_modelos()  # Lineal, Random Forest, LightGBM
             →  evaluar_modelos()   # RMSE, MAE, R²
             →  guardar_mejor_modelo()
```

**Target**: `value_eur`  
**Métrica objetivo**: R² > 0.75, RMSE < 3M EUR  
**Modelo esperado**: Random Forest Regressor o LightGBM

### FASE 4: API REST (backend/api/)
FastAPI con 6 endpoints principales
- Búsqueda y filtrado
- Predicciones ML
- Datos para dashboard

### FASE 5: DASHBOARD (frontend/)
Streamlit con 4 tabs:
1. 🔍 Búsqueda de Jugadores
2. 📊 Análisis de Mercado
3. 🤖 Predictor de Valor
4. 💎 Jugadores Infravalorados

---

## 🛠️ TECNOLOGÍAS Y HERRAMIENTAS

### Core
- **Python 3.9+**
- **pandas 2.x** - Manipulación de datos
- **numpy 2.x** - Operaciones numéricas

### Machine Learning
- **scikit-learn** - Preprocessing, modelos, métricas
- **lightgbm** - Gradient boosting (modelo optimizado)
- **joblib** - Serialización

### Web Frameworks
- **FastAPI** - API REST backend
- **Streamlit** - Dashboard frontend
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación

### Visualización
- **plotly** - Gráficos interactivos
- **matplotlib** - Visualizaciones estáticas
- **seaborn** - Gráficos estadísticos

### DevOps
- **Docker** - Contenedorización
- **docker-compose** - Orquestación
- **venv** - Entornos virtuales

---

## 📁 ESTRUCTURA DE CARPETAS

```
proyecto_scouting_fifa/
│
├── venv/                                    # ← Entorno virtual
│
├── datos/
│   ├── crudos/
│   │   └── fifa.xlsx                        # ← Dataset original (ya disponible)
│   └── procesados/
│       └── jugadores_limpios.csv            # ← Generado por pipeline
│
├── backend/
│   ├── pipeline/                            # ← FASE 1
│   │   ├── main.py
│   │   └── scripts/
│   │       ├── carga_datos.py
│   │       ├── limpieza_datos.py
│   │       ├── imputacion_datos.py
│   │       ├── nuevas_caracteristicas.py
│   │       └── guardado_datos.py
│   │
│   ├── eda/                                 # ← FASE 2
│   │   └── notebooks/
│   │       ├── exploracion.ipynb
│   │       ├── visualizaciones.ipynb
│   │       └── analisis_correlaciones.ipynb
│   │
│   ├── ml/                                  # ← FASE 3
│   │   ├── entrenar.py
│   │   ├── scripts/
│   │   │   ├── preprocesamiento_ml.py
│   │   │   ├── entrenamiento_modelo.py
│   │   │   └── guardado_modelo.py
│   │   └── modelos/
│   │       ├── modelo_regresion.joblib      # ← Generado
│   │       └── encoder.joblib               # ← Generado
│   │
│   └── api/                                 # ← FASE 4
│       ├── api_app.py
│       └── requirements-api.txt
│
├── frontend/                                # ← FASE 5
│   ├── dashboard_app.py
│   └── requirements-dashboard.txt
│
├── documentacion/
│   ├── PROPUESTA.md                         # ← AGENTeS.md mejorado
│   ├── RESUMEN_EJECUTIVO.md                 # ← Este archivo
│   └── ANALISIS_TECNICO.md
│
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   └── docker-compose.yml
│
├── requirements.txt                         # ← Todas las dependencias
├── .gitignore
└── README.md
```

---

## 🎨 CONVENCIONES DE CÓDIGO

### Estilo
- ✅ **snake_case** para todo
- ✅ **Español** para nombres
- ✅ **Docstrings** explicativos
- ✅ **Programación funcional y modular**
- ✅ **Código sencillo y directo**

### Ejemplos
```python
# ✅ CORRECTO
def cargar_datos_fifa(ruta_archivo):
    """
    Carga el dataset de FIFA desde un archivo Excel.
    
    Args:
        ruta_archivo: ruta al archivo .xlsx
        
    Returns:
        DataFrame con los datos cargados
    """
    dataframe_jugadores = pd.read_excel(ruta_archivo)
    return dataframe_jugadores

# ❌ INCORRECTO (inglés, camelCase)
def loadFifaData(filePath):
    df = pd.read_excel(filePath)
    return df
```

---

## 🚀 PLAN DE INICIO

### Paso 1: Preparar el Entorno
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias base
pip install pandas numpy openpyxl scikit-learn lightgbm fastapi uvicorn streamlit plotly seaborn joblib
```

### Paso 2: Crear Estructura de Carpetas
```powershell
mkdir datos\crudos, datos\procesados
mkdir backend\pipeline\scripts
mkdir backend\eda\notebooks
mkdir backend\ml\scripts, backend\ml\modelos
mkdir backend\api
mkdir frontend
mkdir documentacion
mkdir docker
```

### Paso 3: Mover Dataset
```powershell
# Mover fifa.xlsx a la ubicación correcta
move fifa.xlsx datos\crudos\
```

### Paso 4: Comenzar con el Pipeline
1. Crear `backend/pipeline/scripts/carga_datos.py`
2. Crear `backend/pipeline/scripts/limpieza_datos.py`
3. Crear `backend/pipeline/main.py`
4. Ejecutar pipeline inicial

---

## ❓ PREGUNTAS Y RESPUESTAS

### P: ¿Qué diferencia hay con el proyecto de videojuegos?
**R**: La estructura, tecnologías y forma de programar son IDÉNTICAS. Solo cambia:
- Dataset: FIFA en lugar de videojuegos
- Target: value_eur en lugar de total_sales
- Features: atributos de jugadores en lugar de características de juegos
- Dominio: fútbol en lugar de gaming

### P: ¿Qué modelo de ML usaremos?
**R**: Regresión. Comenzaremos con Regresión Lineal (baseline), luego Random Forest Regressor y finalmente LightGBM para optimización.

### P: ¿Cómo se identifican jugadores infravalorados?
**R**: Comparando `value_eur` (valor real) con la predicción del modelo. Si predicción > valor real, el jugador está infravalorado.

### P: ¿Cuántos endpoints tendrá la API?
**R**: 6 endpoints principales (ver arquitectura arriba).

### P: ¿Cuántos tabs tendrá el dashboard?
**R**: 4 tabs: Búsqueda, Análisis EDA, Predicción ML, Jugadores Infravalorados.

### P: ¿Trabajamos con venv siempre?
**R**: ✅ SÍ, SIEMPRE con entorno virtual (venv).

---

## ✅ CHECKLIST DE VALIDACIÓN

Antes de comenzar, verifica:
- [ ] Dataset `fifa.xlsx` disponible (✅ YA LO TENEMOS)
- [ ] Proyecto de ejemplo revisado (✅ en carpeta ejercicio_en_clase/)
- [ ] Propuesta leída y entendida (AGENTeS.md)
- [ ] Python 3.9+ instalado
- [ ] Git configurado
- [ ] VS Code o editor preparado

Para cada fase:
- [ ] Pipeline: Dataset limpio generado
- [ ] EDA: Notebooks con visualizaciones
- [ ] ML: Modelo entrenado con R² > 0.75
- [ ] API: 6 endpoints funcionando
- [ ] Dashboard: 4 tabs interactivos

---

## 📞 PRÓXIMOS PASOS

1. **Confirmar entendimiento** de la propuesta
2. **Crear entorno virtual** (venv)
3. **Crear estructura de carpetas**
4. **Comenzar Fase 1**: Pipeline de datos
5. **Avanzar fase por fase** siguiendo el plan

---

## 💡 NOTAS IMPORTANTES

⚠️ **El dataset ya tiene value_eur en formato numérico** (no texto como "€2.5M"), lo cual simplifica la limpieza.

⚠️ **Algunas columnas tienen muchos nulos** pero son esperadas (ej: atributos de portero para jugadores de campo).

⚠️ **La columna `player_positions`** puede tener múltiples posiciones separadas por comas (ej: "CDM, CM"), necesitaremos procesarla.

⚠️ **El modelo debe considerar la posición** al predecir valor, ya que un delantero con Overall 80 vale más que un defensa con Overall 80.

✅ **Seguimos el MISMO enfoque** que el proyecto de videojuegos: modular, funcional, español, snake_case.

================================================================================
FIN DEL RESUMEN EJECUTIVO
================================================================================
