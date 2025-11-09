# 🎯 Sistema de Scouting y Valoración FIFA

Sistema inteligente de scouting para identificar jugadores infravalorados mediante Machine Learning.

---

## 📋 Descripción

Este proyecto implementa un sistema completo de análisis y predicción del valor de mercado de jugadores de fútbol, utilizando datos del videojuego FIFA 21 con 16,155 jugadores y 106 atributos.

### Objetivo Principal
Predecir el **valor de mercado** (`value_eur`) de jugadores mediante regresión y detectar oportunidades (jugadores infravalorados).

---

## 🏗️ Estructura del Proyecto

```
proyecto_scouting_fifa/
├── venv/                              # Entorno virtual Python
├── datos/                             # Datasets
│   ├── fifa.xlsx                      # Dataset original
│   └── fifa_limpio.csv               # Dataset procesado
├── backend/
│   ├── pipeline_limpieza_datos.py    # Pipeline de limpieza
│   ├── entrenamiento.py              # Entrenamiento ML
│   ├── scripts/
│   │   ├── limpieza/                 # 6 módulos de limpieza
│   │   │   ├── cargador_datos.py
│   │   │   ├── limpieza_datos.py
│   │   │   ├── imputacion_datos.py
│   │   │   ├── nuevas_caracteristicas.py
│   │   │   ├── renombrado_columnas.py
│   │   │   └── guardado_datos.py
│   │   └── ml/                       # 3 módulos de ML
│   │       ├── preprocesamiento_modelo.py
│   │       ├── entrenamiento_modelo.py
│   │       └── guardado_modelo.py
│   └── models/                       # Modelos entrenados
│       ├── modelo_fifa.joblib
│       └── encoder_fifa.joblib
├── frontend/
│   └── dashboard_app.py              # Dashboard Streamlit
├── notebooks/                        # Análisis exploratorio
│   └── eda_fifa_scouting.ipynb
├── documentacion/                    # Documentación técnica
│   ├── resumen_eda.md
│   └── resumen_entrenamiento.md
└── requirements.txt                  # Dependencias
```

---

## 🚀 Instalación y Uso

### 1. Crear y activar entorno virtual

```powershell
# Crear venv
python -m venv venv

# Activar venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Pipeline de Limpieza

```powershell
python backend/pipeline_limpieza_datos.py
```

**Resultado**: Genera `datos/fifa_limpio.csv` con 122,501 jugadores procesados

### 3. Entrenar Modelo ML

```powershell
python backend/entrenamiento.py
```

**Resultado**: Genera modelos en `backend/models/`
- `modelo_fifa.joblib` - LightGBM entrenado (R²=0.4753)
- `encoder_fifa.joblib` - OneHotEncoder para categóricas

### 4. Iniciar API

```powershell
uvicorn backend.api_app:app --reload
```

**API disponible en**: http://localhost:8000  
**Documentación**: http://localhost:8000/docs

### 5. Iniciar Dashboard

```powershell
streamlit run frontend/dashboard_app.py
```

**Dashboard disponible en**: http://localhost:8501

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
- Preprocesa 14 features (11 numéricas + 3 categóricas)
- Aplica OneHotEncoding a categóricas
- Divide datos 75/25 (train/test)
- Entrena 3 modelos: Regresión Lineal, Random Forest, LightGBM
- Selecciona mejor modelo por R² (LightGBM: 47.53%)
- Guarda modelo y encoder con joblib

### 3. API REST (`backend/api_app.py`)
Endpoints:
- `GET /jugadores/buscar` - Buscar jugadores con filtros
- `POST /ml/predecir` - Predecir valor de mercado
- `GET /jugadores/infravalorados` - Top jugadores infravalorados

### 4. Dashboard (`frontend/dashboard_app.py`)
3 pestañas interactivas:
- **🔍 Búsqueda**: Filtros + tabla + tarjeta especial de jugador
- **🤖 Predicción**: Formulario para predecir valor
- **💎 Infravalorados**: Oportunidades de mercado

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

- **Lenguaje**: Python 3.9+
- **Procesamiento**: pandas, numpy, openpyxl
- **ML**: scikit-learn, lightgbm, joblib
- **API**: FastAPI, uvicorn, pydantic
- **Dashboard**: Streamlit, plotly
- **Entorno**: venv

---

## 📦 Dependencias Principales

```txt
pandas==2.x
numpy==2.x
openpyxl==3.x
scikit-learn==1.3+
lightgbm==4.x
joblib==1.x
fastapi==0.100+
uvicorn==0.20+
streamlit==1.25+
plotly==5.x
requests==2.31+
```

---

## 📈 Flujo de Trabajo

```
1. Dataset crudo (fifa.xlsx)
        ↓
2. Pipeline limpieza (main.py)
        ↓
3. Dataset procesado (fifa_limpio.csv)
        ↓
4. Entrenamiento ML (train.py)
        ↓
5. Modelo entrenado (.joblib)
        ↓
6. API + Dashboard (predicciones e insights)
```

---

## 🎯 Criterios de Éxito

- ✅ Pipeline procesa 16,155 jugadores correctamente
- ✅ Dataset limpio con < 5% valores nulos
- ✅ Modelo alcanza R² > 0.75
- ✅ API responde en < 1 segundo
- ✅ Dashboard interactivo y funcional
- ✅ Identifica jugadores infravalorados

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

## 🐳 Docker (Opcional)

```powershell
# Construir imagen
docker build -t fifa-scouting .

# Ejecutar contenedor
docker run -p 8000:8000 -p 8501:8501 fifa-scouting
```

---

**¡Sistema listo para identificar las mejores oportunidades del mercado futbolístico!** ⚽🚀
