# ⚽ Sistema de Scouting y Valoración de Jugadores FIFA

**Sistema inteligente de análisis y predicción del valor de mercado de jugadores de fútbol mediante Machine Learning**

---

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema completo de scouting y valoración** de jugadores de fútbol utilizando técnicas de **Aprendizaje Supervisado (Regresión)** sobre datos históricos del videojuego FIFA (versiones 2015-2021).

### 🎯 Objetivo Principal
Predecir el **valor de mercado** (`valor_mercado_eur`) de jugadores profesionales y detectar **oportunidades de mercado** (jugadores infravalorados con alto potencial).

### 📊 Dataset
- **Fuente**: Datos FIFA 2015-2021 (7 hojas de Excel consolidadas)
- **Registros**: 122,501 jugadores únicos
- **Atributos**: 73 columnas tras limpieza (originalmente 106)
- **Formato**: Excel multi-hoja (`fifa.xlsx`)

### 🔬 Tipo de Problema
**Aprendizaje Supervisado - Regresión**

### 🤖 Técnica de Machine Learning
**Random Forest Regressor**
- Modelo ganador con R² = 0.65 - 0.98 (65% - 98% de precisión)
- 4000 estimadores (árboles) con max_depth=30
- Superó a Regresión Lineal (baseline)
- Optimizado para grandes volúmenes de datos con múltiples features

---

## 🏗️ Estructura del Proyecto

```
seminario-complexivo-grupo-7/
│
├── 📁 venv/                                    # Entorno virtual Python (local)
│
├── 📁 datos/                                   # Datasets y modelos (externos a Docker)
│   ├── originales/
│   │   └── fifa.xlsx                          # Dataset original (7 hojas FIFA 15-21)
│   ├── procesados/
│   │   └── fifa_limpio.csv                    # Dataset limpio (122,501 jugadores)
│   └── modelos/                               # Modelos ML entrenados
│       ├── modelo_fifa.joblib                 # Random Forest (500-800 MB)
│       ├── encoder_fifa.joblib                # OneHotEncoder (5-10 MB)
│       └── club_encoding_fifa.joblib          # Encoding de clubes (100-200 KB)
│
├── 📁 backend/                                 # Lógica de procesamiento y ML
│   ├── pipeline_limpieza_datos.py             # 🔧 Pipeline completo de limpieza
│   ├── entrenamiento.py                       # 🤖 Entrenamiento de modelos ML
│   ├── api_scouting_fifa.py                   # 🌐 API REST (FastAPI)
│   │
│   ├── scripts/
│   │   ├── limpieza/                          # 6 módulos de limpieza
│   │   │   ├── cargador_datos.py             # Carga multi-hoja Excel
│   │   │   ├── renombrado_columnas.py        # Traducción al español
│   │   │   ├── limpieza_datos.py             # Eliminación duplicados/nulos
│   │   │   ├── imputacion_datos.py           # Imputación por posición
│   │   │   ├── nuevas_caracteristicas.py     # Ingeniería de features
│   │   │   └── guardado_datos.py             # Exportación CSV
│   │   │
│   │   └── ml/                                # 3 módulos de ML
│   │       ├── preprocesamiento_modelo.py    # Selección/encoding features
│   │       ├── entrenamiento_modelo.py       # Training 2 modelos (LR + RF)
│   │       └── guardado_modelo.py            # Persistencia .joblib
│
├── 📁 frontend/                               # Interfaz de usuario
│   └── dashboard_scouting_fifa.py            # 📊 Dashboard Streamlit
│
├── 📁 eda/                                    # Análisis Exploratorio
│   └── eda_fifa_scouting.ipynb               # 📓 Jupyter Notebook (EDA completo)
│
├── 📁 docker/                                 # Configuración Docker
│   ├── Dockerfile.backend                    # Imagen API
│   ├── Dockerfile.frontend                   # Imagen Dashboard
│   ├── docker-compose.yml                    # Orquestación servicios
│   └── README.md                             # Guía Docker
│
├── 📁 documentos/                             # Documentación y archivos auxiliares
│   └── (archivos y documentos varios del proyecto)
│
├── requirements.txt                          # Dependencias Python completas
└── README.md                                 # Este archivo
```

---

## 🚀 Guía de Instalación y Ejecución

### 📋 Requisitos Previos
- Python 3.9+
- Docker y Docker Compose (para despliegue contenedorizado)
- 2GB de espacio en disco

---

## 🔄 Flujo de Trabajo Completo

### **FASE 1: Preparación del Entorno (venv)**

#### 1.1 Crear y activar entorno virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar todas las dependencias
pip install -r requirements.txt
```

> **Nota**: SIEMPRE trabajar con el entorno virtual activado para los siguientes pasos.

---

### **FASE 2: Procesamiento de Datos (venv)**

#### 2.1 Ejecutar Pipeline de Limpieza

```powershell
# Desde la carpeta backend
cd backend
python pipeline_limpieza_datos.py
```

**📤 Salida generada:**
- `datos/procesados/fifa_limpio.csv` (122,501 jugadores procesados)

**✅ Procesos ejecutados:**
1. Carga 7 hojas Excel (FIFA 15-21)
2. Unifica datos en un solo DataFrame
3. Renombra columnas al español
4. Elimina duplicados y columnas con >70% nulos
5. Normaliza valores monetarios (M, K → euros)
6. Normaliza fechas (ISO 8601)
7. Imputa nulos según posición del jugador
8. Crea 7 nuevas características (ingeniería)

---

### **FASE 3: Análisis Exploratorio de Datos (venv)**

#### 3.1 Ejecutar Notebook EDA

```powershell
# Abrir Jupyter Notebook
jupyter notebook eda/eda_fifa_scouting.ipynb
```

**📊 Análisis realizados en el EDA:**
- Estadísticas descriptivas (distribuciones, outliers)
- Correlaciones entre atributos y valor de mercado
- Visualizaciones (histogramas, boxplots, scatter plots)
- Identificación de features más relevantes para el modelo
- Análisis de categorías (posiciones, ligas, clubes)

**🎯 Objetivo del EDA:**
Determinar qué variables incluir en el entrenamiento del modelo ML.

---

### **FASE 4: Entrenamiento de Modelos (venv)**

#### 4.1 Entrenar modelos ML

```powershell
# Desde la carpeta backend
cd backend
python entrenamiento.py
```

**📤 Modelos generados:**
- `datos/modelos/modelo_fifa.joblib` - Random Forest (500-800 MB)
- `datos/modelos/encoder_fifa.joblib` - OneHotEncoder (5-10 MB)
- `datos/modelos/club_encoding_fifa.joblib` - Encoding clubes (100-200 KB)

**🤖 Modelos entrenados y comparados:**
1. Regresión Lineal (baseline)
2. **Random Forest Regressor** ← Seleccionado (mejor rendimiento)

**📈 Configuración del modelo ganador:**
- **Arquitectura**: 4000 árboles (estimadores)
- **Profundidad máxima**: 30 niveles
- **Features**: ~84 (14 numéricas + 70 categóricas tras OneHotEncoding)
- **Tiempo de entrenamiento**: 10-15 minutos
- **R² Score**: 0.65 - 0.98 (65% - 98% de precisión)
- **Validación OOB**: Score interno para robustez
- **MAE y RMSE**: Calculados sobre conjunto de prueba

---

### **FASE 5: Despliegue con Docker**

> **Importante**: La API y el Dashboard se ejecutan en **contenedores Docker** con acceso a los datos procesados (`datos/` montado como volumen externo).

#### 5.1 Levantar servicios con Docker Compose (Recomendado)

```powershell
# Ir a la carpeta docker
cd docker

# Construir y levantar servicios
docker-compose up --build

# O en segundo plano (detached mode)
docker-compose up -d --build
```

**🌐 Servicios disponibles:**
- **API REST**: http://localhost:8000
  - Documentación interactiva: http://localhost:8000/docs
- **Dashboard Streamlit**: http://localhost:8501

#### 5.2 Detener servicios

```powershell
# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

### **ALTERNATIVA: Ejecución Local sin Docker (venv)**

Si prefieres ejecutar API y Dashboard localmente (sin Docker):

#### Opción A: Iniciar API

```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Ejecutar API
cd backend
uvicorn api_scouting_fifa:app --reload --host 0.0.0.0 --port 8000
```

#### Opción B: Iniciar Dashboard

```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Ejecutar Dashboard
cd frontend
streamlit run dashboard_scouting_fifa.py
```

---

## � Despliegue con Docker

### Opción A: Docker Compose (Recomendado)

```powershell
# Ir a la carpeta docker
cd docker

# Levantar servicios
docker-compose up --build

# En segundo plano
docker-compose up -d --build
```

**Acceso:**
- API: http://localhost:8000
- Dashboard: http://localhost:8501

### Opción B: Contenedores Individuales

```powershell
# Backend
docker build -f docker/Dockerfile.backend -t fifa-backend .
docker run -d -p 8000:8000 --name backend fifa-backend

# Frontend
docker build -f docker/Dockerfile.frontend -t fifa-frontend .
docker run -d -p 8501:8501 --name frontend fifa-frontend
```

**Ver documentación completa**: [docker/README.md](docker/README.md)

---

##  Componentes del Sistema

### 1. Pipeline de Datos (`backend/pipeline_limpieza_datos.py`)
- Carga 7 hojas de Excel (FIFA 15-21)
- Unifica y limpia 122,501 registros
- Normaliza valores monetarios y fechas
- Imputa valores nulos por posición
- Crea 5 nuevas características (ingeniería)
- Guarda dataset procesado en español

### 2. Modelo ML (`backend/entrenamiento.py`)
- Preprocesa ~84 features (14 numéricas base + categóricas expandidas)
- Aplica OneHotEncoding a: posición, club, liga, pie preferido, categorías
- Incluye club_encoding para 954 clubes únicos
- Divide datos 75/25 (train/test)
- Entrena 2 modelos: Regresión Lineal (baseline) + Random Forest (principal)
- Selecciona mejor modelo por R² (Random Forest: 65-98%)
- Configuración RF: 4000 estimadores, max_depth=30, validación OOB
- Guarda 3 archivos: modelo + encoder + club_encoding con joblib
- Tiempo: 10-15 minutos para entrenamiento completo

### 3. API REST (`backend/api_scouting_fifa.py`)
8 endpoints disponibles:
- `GET /` - Health check del sistema
- `GET /jugadores/buscar` - Buscar jugadores con filtros avanzados
- `POST /ml/predecir` - Predecir valor de mercado usando Random Forest
- `GET /jugadores/infravalorados` - Top jugadores con mejor potencial/valor
- `GET /clubes` - Listar todos los clubes disponibles
- `GET /ligas` - Listar todas las ligas disponibles
- `GET /posiciones` - Listar todas las posiciones disponibles
- `GET /estadisticas` - Estadísticas generales del dataset

### 4. Dashboard (`frontend/dashboard_scouting_fifa.py`)
3 pestañas interactivas:
- **🔍 Búsqueda y Análisis**: Filtros avanzados + tabla de resultados + tarjeta especial de jugador con gráfico radar
- **📊 Análisis de Mercado**: Visualizaciones de distribución de valores, análisis por liga/posición
- **🤖 Predicción ML**: Formulario interactivo para predecir valor de mercado usando Random Forest

---

## 🎨 Características Especiales

### Tarjeta de Jugador
Cuando se selecciona un jugador, muestra:
- Foto/imagen
- Datos básicos (nombre, club, posición)
- Métricas (overall, potencial, valor)
- **Gráfico radar** con 6 atributos principales
- Link al perfil completo

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11
- **Procesamiento**: pandas 2.3.3, numpy 2.3.4, openpyxl 3.1.5
- **ML**: scikit-learn 1.7.2, joblib 1.4.2
- **API**: FastAPI 0.121.1, uvicorn 0.38.0, pydantic 2.10.6
- **Dashboard**: Streamlit 1.50.0, plotly 6.4.0
- **Contenedores**: Docker + Docker Compose
- **Entorno**: venv (desarrollo local)

---

## 📦 Dependencias Principales

```txt
# Procesamiento de datos
pandas==2.3.3
numpy==2.3.4
openpyxl==3.1.5

# Machine Learning
scikit-learn==1.7.2
joblib==1.4.2

# API Backend
fastapi==0.121.1
uvicorn==0.38.0
pydantic==2.10.6

# Dashboard Frontend
streamlit==1.50.0
plotly==6.4.0

# Notebooks (EDA)
jupyter==7.0.1
notebook==7.3.2
```

---

## 📈 Flujo de Trabajo

```
1. Dataset crudo (datos/originales/fifa.xlsx - 7 hojas Excel)
        ↓
2. Pipeline limpieza (backend/pipeline_limpieza_datos.py - 7 etapas)
        ↓
3. Dataset procesado (datos/procesados/fifa_limpio.csv - 122,501 jugadores)
        ↓
4. Análisis EDA (eda/eda_fifa_scouting.ipynb - Jupyter Notebook)
        ↓
5. Entrenamiento ML (backend/entrenamiento.py - Random Forest 4000 árboles)
        ↓
6. Modelos entrenados (datos/modelos/*.joblib - 3 archivos)
        ↓
7. API + Dashboard (Docker: backend:8000 + frontend:8501)
        ↓
8. Predicciones y análisis en tiempo real
```

---

## 🎯 Criterios de Éxito

- ✅ Pipeline procesa 122,501 jugadores correctamente
- ✅ Dataset limpio con 73 columnas (eliminadas 33 con >70% nulos)
- ✅ Modelo alcanza R² > 0.65 (Random Forest con 4000 árboles)
- ✅ Validación OOB confirma robustez del modelo
- ✅ API con 8 endpoints funcionales (responde en < 1 segundo)
- ✅ Dashboard con 3 pestañas interactivas
- ✅ Identifica jugadores infravalorados con alta precisión
- ✅ Sistema completamente dockerizado y listo para producción

---

## 👥 Equipo

- Alberto Alexander Aldás Villacrés
- Cristian Joel Riofrío Medina
- Wilson Fernando Saavedra Álvarez

**Asignatura**: Analítica con Python  
**Institución**: UniAndes  
**Fecha**: Noviembre 2025

---

## 📝 Notas

- **SIEMPRE** trabajar con `venv` activado
- Seguir convenciones: `snake_case` en español
- Código simple, directo y funcional
- Basado en el proyecto del profesor (ejercicio_en_clase)

---

## 🐳 Arquitectura Docker

### Ventajas del Enfoque Actual

✅ **Datos externos**: `datos/` se monta como volumen (no se reconstruye el contenedor al actualizar datos)  
✅ **Optimización**: Imágenes Docker ligeras (solo contienen código, no datasets)  
✅ **Escalabilidad**: API y Dashboard independientes  
✅ **Persistencia**: Modelos entrenados (.joblib) accesibles por ambos servicios

### Contenedores

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| `backend` | 8000 | API REST (FastAPI) |
| `frontend` | 8501 | Dashboard (Streamlit) |

### Volúmenes Montados

```yaml
volumes:
  - ../datos:/app/datos:ro  # Datos externos read-only (originales + procesados + modelos)
```

**Contenido montado:**
- `datos/originales/fifa.xlsx` (dataset original)
- `datos/procesados/fifa_limpio.csv` (122,501 jugadores limpios)
- `datos/modelos/modelo_fifa.joblib` (Random Forest 500-800 MB)
- `datos/modelos/encoder_fifa.joblib` (OneHotEncoder 5-10 MB)
- `datos/modelos/club_encoding_fifa.joblib` (Encoding clubes 100-200 KB)

---

## 📊 Componentes del Sistema

### 1. Pipeline de Limpieza (`backend/pipeline_limpieza_datos.py`)
**Entrada**: `datos/originales/fifa.xlsx` (7 hojas)  
**Salida**: `datos/procesados/fifa_limpio.csv`

**Transformaciones aplicadas:**
- ✅ Unificación de 7 hojas (FIFA 15-21)
- ✅ Renombrado de 106 → 73 columnas (español)
- ✅ Eliminación de duplicados
- ✅ Normalización monetaria (M, K → EUR)
- ✅ Normalización temporal (fechas ISO 8601)
- ✅ Imputación inteligente por posición
- ✅ Creación de 7 nuevas features:
  - `calidad_promedio` (mean de atributos)
  - `diferencia_potencial` (potential - overall)
  - `categoria_edad` (joven/consolidado/veterano)
  - `categoria_posicion` (delantero/medio/defensa/portero)
  - `ratio_valor_salario` (value/wage)
  - `anos_contrato_restantes`
  - `categoria_reputacion` (baja/media/alta/estrella)

---

### 2. Análisis Exploratorio (`eda/eda_fifa_scouting.ipynb`)
**Objetivo**: Descubrir patrones y seleccionar features para ML

**Visualizaciones clave:**
- Distribución de valores de mercado
- Correlación entre atributos técnicos y precio
- Análisis por posición, liga, edad
- Detección de outliers

---

### 3. Entrenamiento ML (`backend/entrenamiento.py`)
**Variable objetivo**: `valor_mercado_eur`

**Features utilizadas (14 totales):**
- **Numéricas (11)**: overall, potencial, edad, calidad_promedio, etc.
- **Categóricas (3)**: posición, pie_preferido, categoria_edad (OneHotEncoding)

**Proceso:**
1. Preprocesamiento (encoding, split 75/25)
2. Entrenamiento de 3 modelos
3. Evaluación y selección del mejor
4. Guardado de modelo + encoder

**Modelo ganador**: Random Forest (R²=0.65-0.98, 4000 estimadores, max_depth=30)

---

### 4. API REST (`backend/api_scouting_fifa.py`)

**Tecnología**: FastAPI + Uvicorn

**Endpoints principales:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/jugadores/buscar` | Búsqueda con filtros |
| POST | `/ml/predecir` | Predecir valor de mercado |
| GET | `/jugadores/infravalorados` | Top jugadores infravalorados |

**Ejemplo de uso:**

```bash
# Predecir valor de un jugador
curl -X POST "http://localhost:8000/ml/predecir" \
  -H "Content-Type: application/json" \
  -d '{
    "overall": 85,
    "potencial": 90,
    "edad": 23,
    "posicion": "Delantero"
  }'
```

---

### 5. Dashboard (`frontend/dashboard_scouting_fifa.py`)

**Tecnología**: Streamlit + Plotly

**Pestañas disponibles:**

| Pestaña | Funcionalidad |
|---------|---------------|
| 🔍 **Búsqueda** | Filtros interactivos + tabla de resultados |
| 🤖 **Predicción ML** | Formulario para predecir valor de mercado |
| 💎 **Infravalorados** | Top oportunidades del mercado |

**Características especiales:**
- Tarjetas de jugador con gráficos radar
- Filtros por posición, liga, club, edad
- Visualizaciones interactivas con Plotly
- Integración con API para predicciones en tiempo real

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.11** (imagen base Docker: python:3.11-slim)
- **Pandas 2.3.3** - Procesamiento de datos
- **NumPy 2.3.4** - Operaciones numéricas
- **Scikit-learn 1.7.2** - Random Forest y preprocesamiento ML
- **Joblib 1.4.2** - Serialización de modelos
- **FastAPI 0.121.1** - Framework API REST
- **Uvicorn 0.38.0** - Servidor ASGI
- **Pydantic 2.10.6** - Validación de datos

### Frontend
- **Streamlit 1.50.0** - Framework de dashboards
- **Plotly 6.4.0** - Visualizaciones interactivas

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación multi-contenedor

### Data Science
- **Jupyter 7.0.1** - Notebooks para EDA
- **OpenPyXL 3.1.5** - Lectura de archivos Excel

---

## 📈 Resultados del Modelo

| Modelo | R² Score | Configuración | Seleccionado |
|--------|----------|---------------|--------------|
| Regresión Lineal | ~0.35-0.45 | Baseline (fit_intercept=True, n_jobs=-1) | ❌ |
| **Random Forest** | **0.65-0.98** | 4000 estimadores, max_depth=30, min_samples_split=10 | ✅ |

**Interpretación**: El modelo Random Forest explica entre el 65% y 98% de la variabilidad en el valor de mercado de los jugadores, dependiendo del rango de precios.

**Características técnicas del modelo ganador:**
- **4000 árboles de decisión** para máxima estabilidad
- **84 features** (14 numéricas + 70 categóricas tras OneHotEncoding)
- **Validación OOB** (Out-of-Bag) para verificar robustez sin cross-validation
- **Tiempo de entrenamiento**: 10-15 minutos en CPU multi-core
- **Tamaño del modelo**: 500-800 MB en disco

---

## 🎯 Casos de Uso

1. **Scouts deportivos**: Identificar jugadores con potencial infravalorado
2. **Clubes de fútbol**: Optimizar inversiones en fichajes
3. **Analistas deportivos**: Comprender qué factores determinan el valor de mercado
4. **Videojugadores FIFA**: Estrategias para el modo carrera/Ultimate Team

---

## 👥 Equipo

- **Alberto Alexander Aldás Villacrés**
- **Cristian Joel Riofrío Medina**
- **Wilson Fernando Saavedra Álvarez**

**Asignatura**: Analítica con Python  
**Institución**: Universidad Regional Autónoma de los Andes (UniAndes)  
**Fecha**: Noviembre 2025

---

## 📝 Licencia y Notas

- Dataset FIFA utilizado únicamente con fines académicos
- Proyecto desarrollado como caso de estudio para aprendizaje de ML
- **Tipo de problema**: Aprendizaje Supervisado - Regresión
- **Técnica principal**: Random Forest Regressor (4000 árboles)
- **Precisión**: R² entre 0.65 y 0.98 (65%-98%)

---

**⚽ ¡Sistema listo para identificar las mejores oportunidades del mercado futbolístico! 🚀**
