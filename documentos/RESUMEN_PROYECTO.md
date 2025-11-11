# RESUMEN DEL PROYECTO: SISTEMA DE SCOUTING FIFA

## Información General

**Proyecto**: Sistema de Scouting Inteligente y Valoración de Jugadores de Fútbol
**Asignatura**: Analítica con Python
**Fecha de Finalización**: 9 de noviembre de 2025
**Estado**: COMPLETADO EXITOSAMENTE

## Dataset

- **Fuente**: FIFA 21
- **Total de Jugadores**: 122,501
- **Total de Columnas**: 73 características
- **Tamaño del Archivo**: 51.14 MB (fifa_limpio.csv)
- **Características**: Atributos técnicos, físicos, mentales, información de mercado y demográfica

## Modelo de Machine Learning

### Rendimiento del Modelo
- **Algoritmo**: Random Forest Regressor
- **Métrica R²**: 98.30%
- **MAE (Error Absoluto Medio)**: €333,865
- **Error Relativo**: 13.2% (excelente para el mercado de fútbol)
- **Tamaño del Modelo**: 5.2 GB (modelo_fifa.joblib)

### Hiperparámetros
- n_estimators: 2000
- max_depth: 30
- min_samples_split: 10
- min_samples_leaf: 1
- max_features: sqrt

### Features del Modelo
- **Total de Features**: 110
- **Features Numéricas**: 48 (atributos técnicos, físicos, edad, etc.)
- **Features Categóricas**: 5 (posición, nacionalidad, club, liga, pie preferido)
- **Features Codificadas**: 62 (OneHot encoding)

## API REST (Backend)

### Tecnologías
- **Framework**: FastAPI 0.121.1
- **Servidor**: Uvicorn 0.38.0
- **Puerto**: 8000
- **Validación**: Pydantic 2.12.4

### Endpoints Implementados (9 total)

1. **GET /** - Información general de la API
2. **GET /jugadores/filtros** - Opciones de filtrado disponibles
3. **GET /jugadores/buscar** - Búsqueda de jugadores con filtros personalizables
4. **GET /jugadores/{id}/perfil** - Perfil completo de un jugador con predicción ML
5. **POST /ml/predecir_valor** - Predicción de valor de mercado
6. **GET /jugadores/infravalorados** - Jugadores potencialmente infravalorados
7. **GET /jugadores/sobrevalorados** - Jugadores potencialmente sobrevalorados
8. **GET /eda/estadisticas_generales** - Estadísticas generales del dataset
9. **GET /eda/datos_graficos** - Datos procesados para visualizaciones

### Resultados de Pruebas
- **Total de Tests**: 10
- **Tests Exitosos**: 10/10 (100%)
- **Optimizaciones Implementadas**: Batch prediction, manejo de infinitos, filtrado de valores nulos

## Dashboard (Frontend)

### Tecnologías
- **Framework**: Streamlit 1.50.0
- **Visualizaciones**: Plotly 6.4.0
- **Puerto**: 8501
- **Integración**: API REST
- **Configuración Docker**: Usa variable de entorno `API_BASE_URL` para conectar con backend

### Estructura del Dashboard

#### Tab 1: Exploración de Jugadores
- Filtros laterales: posición, nacionalidad, edad, rating, potencial, valor
- Tabla de resultados con ordenamiento y búsqueda
- Ficha de jugador detallada:
  - Fotografía del jugador
  - Gráfico radar de 6 atributos técnicos
  - Comparación valor real vs predicho
  - Clasificación (infravalorado/justo/sobrevalorado)

#### Tab 2: Análisis de Mercado
- KPIs generales del dataset
- Top 20 clubes más valiosos
- Top 20 ligas por valor total
- Distribución por posiciones
- Top 5 jugadores infravalorados
- Top 5 jugadores sobrevalorados

#### Tab 3: Predicción de Valor
- Formulario interactivo con sliders para todos los atributos
- Predicción en tiempo real
- Percentil del valor predicho
- Gráfico gauge mostrando posición en el mercado

### Paleta de Colores
- Negro: #000000
- Gris-Azul: #7890a8
- Azul Oscuro: #304878
- Azul Muy Oscuro: #181848
- Dorado/Naranja: #f0a818

## Dockerización

### Arquitectura de Contenedores

**Backend Container (fifa-backend)**:
- Base: Python 3.11-slim
- Puerto: 8000
- Dependencias: FastAPI, scikit-learn, pandas, numpy, joblib
- Tamaño: ~5.5 GB (incluye modelo ML)

**Frontend Container (fifa-frontend)**:
- Base: Python 3.11-slim
- Puerto: 8501
- Dependencias: Streamlit, Plotly, requests
- Tamaño: ~800 MB

**Red Docker**:
- Nombre: fifa-network
- Tipo: bridge
- Comunicación: Backend ↔ Frontend

### Configuración de Localización
- **Zona Horaria**: America/Guayaquil (Ecuador)
- **Codificación**: UTF-8 (LANG=C.UTF-8, LC_ALL=C.UTF-8, PYTHONIOENCODING=utf-8)
- **Soporte**: Tildes, ñ y caracteres latinos

### Comandos de Docker

**Construcción y Ejecución**:
```bash
cd docker
docker-compose up --build
```

**Acceso a Servicios**:
- Backend API: http://localhost:8000
- API Documentación: http://localhost:8000/docs
- Dashboard: http://localhost:8501

**Comandos Útiles**:
```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart
```

## Estructura del Proyecto

```
proyecto_scouting_fifa/
├── datos/
│   └── fifa_limpio.csv (51.14 MB)
├── backend/
│   ├── api_scouting_fifa.py (924 líneas)
│   ├── probar_api.py (300 líneas)
│   ├── requirements-api.txt
│   └── models/
│       ├── modelo_fifa.joblib (5.2 GB)
│       ├── encoder_fifa.joblib
│       └── club_encoding_fifa.joblib
├── frontend/
│   ├── dashboard_scouting_fifa.py (800 líneas)
│   ├── requirements-dashboard.txt
│   └── iniciar_dashboard.bat
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── README.md
└── documentacion/
    └── [documentos varios]
```

## Fases Completadas

1. ✅ **Preparación del Entorno**: Configuración de venv y dependencias
2. ✅ **Pipeline de Datos**: Limpieza, imputación y feature engineering
3. ✅ **Análisis Exploratorio**: Visualizaciones y descubrimiento de patrones
4. ✅ **Modelo de ML**: Entrenamiento y optimización (R²=98.30%)
5. ✅ **API REST**: 9 endpoints completamente funcionales
6. ✅ **Dashboard**: Interfaz completa con 3 tabs y visualizaciones interactivas
7. ✅ **Dockerización**: Contenedores backend/frontend con orquestación
8. ✅ **Documentación**: Completa y detallada

## Resultados Clave

### Rendimiento del Modelo
- R² de 98.30% demuestra excelente capacidad predictiva
- MAE de €333,865 es aceptable considerando el rango de valores (€0 - €123M)
- Error relativo de 13.2% es competitivo con mercados financieros

### API REST
- 10/10 tests pasando exitosamente
- Tiempo de respuesta < 1 segundo para predicciones
- Optimización batch reduce tiempo en 4x

### Dashboard
- Interfaz intuitiva y profesional
- Visualizaciones interactivas con Plotly
- Integración fluida con API backend

### Dockerización
- Construcción exitosa en 15 minutos
- Servicios funcionando correctamente
- Configuración UTF-8 y timezone Ecuador

## Criterios de Éxito Alcanzados

| Criterio | Objetivo | Resultado | Estado |
|----------|----------|-----------|--------|
| Dataset procesado | < 5% valores nulos | < 2% | ✅ |
| R² del modelo | > 0.75 | 0.983 | ✅ |
| RMSE del modelo | < €3M | €2.1M | ✅ |
| Tiempo de respuesta API | < 1s | < 0.5s | ✅ |
| Tiempo de carga dashboard | < 3s | < 2s | ✅ |
| Identificación infravalorados | Funcional | 125 encontrados | ✅ |
| Código legible | Modular | Simplificado | ✅ |
| Reproducibilidad | Docker | Funcionando | ✅ |

## Insights del Negocio

### Jugadores Infravalorados Destacados
1. F. Brienza: +292% diferencia (valor real €1.9K, predicho €7.6K)
2. M. Busatto: +288% diferencia
3. G. Monteiro: +278% diferencia

### Jugadores Sobrevalorados Destacados
1. Pau López: -75.6% diferencia (valor real €30M, predicho €7.3M)
2. M. Lanzini: -73.2% diferencia
3. J. Guilavogui: -72.8% diferencia

### Estadísticas Generales
- Total de jugadores: 122,501
- Clubes representados: 954
- Nacionalidades: 182
- Ligas: 56
- Club más valioso: Real Madrid (€5.2B)

## Tecnologías Utilizadas

### Lenguaje
- Python 3.11

### Machine Learning
- scikit-learn (Random Forest)
- pandas (procesamiento de datos)
- numpy (operaciones numéricas)
- joblib (persistencia de modelos)

### Backend
- FastAPI (API REST)
- Uvicorn (servidor ASGI)
- Pydantic (validación)

### Frontend
- Streamlit (dashboard)
- Plotly (visualizaciones)
- requests (integración API)

### Infraestructura
- Docker (contenedorización)
- Docker Compose (orquestación)

## Lecciones Aprendidas

1. **Batch ML Predictions**: Procesar en lotes es 4x más rápido que iteración row-by-row
2. **Manejo de Infinitos**: División por cero debe manejarse antes de JSON serialization
3. **Docker con Modelos Grandes**: Transferencia de contexto toma tiempo significativo (~10 minutos)
4. **UTF-8 Configuration**: Requiere múltiples variables de entorno (LANG, LC_ALL, PYTHONIOENCODING)
5. **API Optimization**: Reducir muestras de 10K a 2K mejoró significativamente tiempos de respuesta

## Recomendaciones Futuras

1. **Escalabilidad**: Considerar Kubernetes para producción
2. **Caching**: Implementar Redis para predicciones frecuentes
3. **Modelo**: Reentrenar periódicamente con datos actualizados
4. **Features**: Agregar análisis de tendencias temporales
5. **UI/UX**: Versión móvil del dashboard
6. **Testing**: Ampliar cobertura de tests unitarios
7. **Monitoring**: Agregar métricas de uso y performance

## Contacto

**Proyecto Desarrollado Para**:
- Asignatura: Analítica con Python
- Institución: UniAndes
- Profesor: Juan Felipe Nájera

**Fecha de Entrega**: 9 de noviembre de 2025

---

**ESTADO FINAL**: PROYECTO COMPLETADO EXITOSAMENTE
