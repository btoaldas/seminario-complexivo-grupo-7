# MAPEO COMPLETO DE ARCHIVOS RENOMBRADOS

## 📋 RESUMEN DE CAMBIOS

Todos los archivos `.py` del proyecto han sido renombrados a **español** para mantener consistencia con el código y facilitar la comprensión del equipo hispanohablante.

---

## 🗂️ ARCHIVOS RENOMBRADOS

### Backend - Scripts de Procesamiento de Datos

| Nombre Anterior (Inglés) | Nombre Nuevo (Español) | Propósito |
|--------------------------|------------------------|-----------|
| `data_loader.py` | `cargador_datos.py` | Carga las 7 hojas del Excel FIFA |
| `data_cleaning.py` | `limpieza_datos.py` | Limpia y normaliza los datos |
| `data_imputation.py` | `imputacion_datos.py` | Imputa valores nulos |
| `data_new_features.py` | `nuevas_caracteristicas.py` | Crea características derivadas |
| `data_saving.py` | `guardado_datos.py` | Guarda datos procesados |
| `renombrado_columnas.py` | `renombrado_columnas.py` | ✅ Ya estaba en español |

### Backend - Scripts de Machine Learning

| Nombre Anterior (Inglés) | Nombre Nuevo (Español) | Propósito |
|--------------------------|------------------------|-----------|
| `model_preprocessing.py` | `preprocesamiento_modelo.py` | Prepara datos para entrenamiento |
| `model_training.py` | `entrenamiento_modelo.py` | Entrena modelos de regresión |
| `model_saving.py` | `guardado_modelo.py` | Guarda modelos entrenados |

### Backend - Scripts Principales

| Nombre Anterior (Inglés) | Nombre Nuevo (Español) | Propósito |
|--------------------------|------------------------|-----------|
| `main.py` | `pipeline_limpieza_datos.py` | Pipeline completo de limpieza (6 fases) |
| `train.py` | `entrenamiento_modelo_ml.py` | Script de entrenamiento de ML |
| `api_app.py` | `api_scouting.py` | API REST con FastAPI |

### Frontend

| Nombre Anterior (Inglés) | Nombre Nuevo (Español) | Propósito |
|--------------------------|------------------------|-----------|
| `dashboard_app.py` | `dashboard_scouting.py` | Dashboard interactivo Streamlit |

---

## 🔧 ACTUALIZACIONES REALIZADAS

### 1. Imports Actualizados en `pipeline_limpieza_datos.py`

```python
# ANTES:
from scripts.data_loader import cargar_datos_fifa
from scripts.data_cleaning import seleccionar_columnas_relevantes, eliminar_duplicados
from scripts.data_imputation import imputar_valores_nulos
from scripts.data_new_features import crear_calidad_promedio
from scripts.data_saving import guardar_datos_limpios

# DESPUÉS:
from scripts.cargador_datos import cargar_datos_fifa
from scripts.limpieza_datos import seleccionar_columnas_relevantes, eliminar_duplicados
from scripts.imputacion_datos import imputar_valores_nulos
from scripts.nuevas_caracteristicas import crear_calidad_promedio
from scripts.guardado_datos import guardar_datos_limpios
```

### 2. Imports Actualizados en `entrenamiento_modelo_ml.py`

```python
# ANTES:
from scripts.model_preprocessing import preparar_datos_para_ml
from scripts.model_training import entrenar_random_forest, entrenar_lightgbm
from scripts.model_saving import guardar_modelo, guardar_encoder

# DESPUÉS:
from scripts.preprocesamiento_modelo import preparar_datos_para_ml
from scripts.entrenamiento_modelo import entrenar_random_forest, entrenar_lightgbm
from scripts.guardado_modelo import guardar_modelo, guardar_encoder
```

### 3. Docker Actualizado

**Dockerfile.backend:**
```dockerfile
# ANTES:
CMD ["uvicorn", "backend.api_app:app", "--host", "0.0.0.0", "--port", "8000"]

# DESPUÉS:
CMD ["uvicorn", "backend.api_scouting:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile.frontend:**
```dockerfile
# ANTES:
CMD ["streamlit", "run", "frontend/dashboard_app.py", "--server.address=0.0.0.0"]

# DESPUÉS:
CMD ["streamlit", "run", "frontend/dashboard_scouting.py", "--server.address=0.0.0.0"]
```

---

## 📂 ESTRUCTURA FINAL DEL PROYECTO

```
proyecto_scouting_fifa/
│
├── datos/
│   ├── fifa.xlsx                      # Dataset original (7 hojas)
│   └── fifa_limpio.csv                # Dataset procesado
│
├── backend/
│   ├── pipeline_limpieza_datos.py     # ⭐ Pipeline principal (era main.py)
│   ├── entrenamiento_modelo_ml.py     # ⭐ Entrenamiento ML (era train.py)
│   ├── api_scouting.py                # ⭐ API REST (era api_app.py)
│   │
│   ├── scripts/
│   │   ├── cargador_datos.py          # ✅ (era data_loader.py)
│   │   ├── renombrado_columnas.py     # ✅ (ya estaba en español)
│   │   ├── limpieza_datos.py          # ✅ (era data_cleaning.py)
│   │   ├── imputacion_datos.py        # ✅ (era data_imputation.py)
│   │   ├── nuevas_caracteristicas.py  # ✅ (era data_new_features.py)
│   │   ├── guardado_datos.py          # ✅ (era data_saving.py)
│   │   ├── preprocesamiento_modelo.py # ✅ (era model_preprocessing.py)
│   │   ├── entrenamiento_modelo.py    # ✅ (era model_training.py)
│   │   └── guardado_modelo.py         # ✅ (era model_saving.py)
│   │
│   └── models/
│       ├── modelo_fifa.joblib
│       └── encoder_fifa.joblib
│
├── frontend/
│   └── dashboard_scouting.py          # ⭐ Dashboard (era dashboard_app.py)
│
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend             # ✅ Actualizado
│   └── Dockerfile.frontend            # ✅ Actualizado
│
└── documentacion/
    ├── MEJORAS_PIPELINE.md
    ├── REORGANIZACION_PIPELINE.md
    └── MAPEO_ARCHIVOS_RENOMBRADOS.md  # 📄 Este documento
```

---

## 🚀 COMANDOS ACTUALIZADOS

### Ejecutar Pipeline de Limpieza

```bash
# ANTES:
python backend/main.py

# DESPUÉS:
python backend/pipeline_limpieza_datos.py
```

### Entrenar Modelo ML

```bash
# ANTES:
python backend/train.py

# DESPUÉS:
python backend/entrenamiento_modelo_ml.py
```

### Ejecutar API

```bash
# ANTES:
uvicorn backend.api_app:app --reload

# DESPUÉS:
uvicorn backend.api_scouting:app --reload
```

### Ejecutar Dashboard

```bash
# ANTES:
streamlit run frontend/dashboard_app.py

# DESPUÉS:
streamlit run frontend/dashboard_scouting.py
```

### Docker Compose (sin cambios)

```bash
# Sigue igual:
docker-compose -f docker/docker-compose.yml up --build
```

---

## ✅ VERIFICACIÓN COMPLETADA

- ✅ Todos los archivos renombrados a español
- ✅ Imports actualizados en `pipeline_limpieza_datos.py`
- ✅ Imports actualizados en `entrenamiento_modelo_ml.py`
- ✅ Dockerfile.backend actualizado
- ✅ Dockerfile.frontend actualizado
- ✅ Documentación creada

---

## 🎯 CONVENCIÓN DE NOMBRES

A partir de ahora, **todos los archivos Python** del proyecto seguirán esta convención:

1. **snake_case** (minúsculas con guiones bajos)
2. **Nombres descriptivos en español**
3. **Verbos que describen la acción principal** (ej: `pipeline_limpieza_datos`, `entrenamiento_modelo_ml`)

### Ejemplos:
- ✅ `cargador_datos.py` → Carga datos
- ✅ `limpieza_datos.py` → Limpia datos
- ✅ `nuevas_caracteristicas.py` → Crea features
- ✅ `pipeline_limpieza_datos.py` → Pipeline completo
- ❌ `data_loader.py` → Nombre en inglés (evitar)
- ❌ `utils.py` → Nombre genérico (evitar)

---

**Fecha de actualización:** 8 de noviembre de 2025  
**Autor:** Equipo de Desarrollo - Sistema de Scouting FIFA  
**Versión:** 1.0
