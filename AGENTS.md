# GUIA DE CODIFICACION - PROYECTO SCOUTING FIFA

---

## REGLAS DE CODIFICACION

### 1. Convenciones de nomenclatura (snake_case)

- TODO en minusculas con guion bajo: funciones, nombres de archivo, variables, constantes, etc.
- Caracteres especiales: 
  - Palabras con ni en lugar de ñ (ejemplo: año -> anio)
  - Omitir tildes en codigo (ejemplo: funcion en lugar de función)
- EXCEPCION: Los comentarios y documentacion SI llevan tildes y mayusculas correctas en español para facilitar la comprension.

Ejemplos:

\\\python
# Correcto
nombre_archivo = "datos_limpios.py"
def calcular_promedio_edad():
    anio_actual = 2025
    
# Incorrecto
nombreArchivo = "datosLimpios.py"
def calcularPromedioEdad():
    añoActual = 2025
\\\

### 2. Organizacion de archivos

- Un archivo por responsabilidad: un archivo para pipeline, otro para machine learning, otro para dashboard.
- Nombres descriptivos: pipeline.py, modelo_random_forest.py, dashboard_streamlit.py

### 3. Documentacion del codigo

- Comentarios obligatorios en cada funcion explicando:
  - Que hace la funcion
  - Parametros que recibe
  - Que retorna
- Usar español latinoamericano con tildes y mayusculas correctas en comentarios

Ejemplo:

\\\python
def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Elimina jugadores duplicados conservando el registro con mayor calificacion.
    
    Args:
        df: DataFrame con datos de jugadores
        
    Returns:
        DataFrame sin duplicados
    \"\"\"
    # codigo aqui
\\\

### 4. Configuracion regional

- Codificacion: UTF-8
- Zona horaria: Guayaquil (America/Guayaquil)
- Idioma: Español latinoamericano

### 5. Limpieza de codigo

- Eliminar codigo obsoleto: scripts de prueba fallidos, codigo comentado innecesario
- Codigo limpio: directo, funcional, eficiente, comprensible, facil de mantener
- Evitar complejidad innecesaria: preferir soluciones simples y claras

### 6. Estructura del proyecto

- Documentacion: archivos .md en /documentos/
- Backups: en /backups/ con la misma estructura
- Respetar arquitectura: mantener coherencia con el codigo existente

---

## VISION GENERAL DEL PROYECTO

### Tema

Sistema de Scouting y Valoracion de Jugadores de Futbol Profesional

### Tipo de aprendizaje

Aprendizaje supervisado - Regresion

### Dataset

Datos del videojuego FIFA 15-21 con cientos de atributos de jugadores.

---

## OBJETIVO GLOBAL

Construir una herramienta que permita:

- Filtrar y analizar jugadores (edad, posicion, nacionalidad, potencial, etc.)
- Predecir su valor de mercado estimado usando un modelo de Machine Learning (regresion)
- Identificar jugadores infravalorados, cuyo valor real sea menor al estimado por el modelo

---

## ETAPAS DEL PROYECTO

| Etapa | Descripcion | Herramientas |
|-------|-------------|--------------|
| 1 Pipeline de datos | Limpieza, unificacion y preparacion del dataset | pandas, numpy |
| 2 EDA (Analisis exploratorio) | Entender correlaciones y relaciones entre variables | seaborn, matplotlib |
| 3 Feature Engineering | Transformar columnas, codificar texto, normalizar | pandas, sklearn.preprocessing |
| 4 Entrenamiento (Regresion) | Crear modelo supervisado para predecir el valor | sklearn.ensemble.RandomForestRegressor |
| 5 Evaluacion del modelo | Validar precision con metricas (MAE, R2) | sklearn.metrics |
| 6 Predicciones e Infravalorados | Comparar valor real vs predicho, detectar oportunidades | pandas |
| 7 API REST (FastAPI) | Exponer modelo y predicciones como servicio | FastAPI, uvicorn, joblib |
| 8 Dashboard (Streamlit) | Visualizar y explorar jugadores e infravalorados | Streamlit, Plotly, Altair |

---

## DETALLE DE ETAPAS

### ETAPA 1 - PIPELINE DE DATOS

Objetivo: Unificar todas las hojas (2015-2021) en un solo DataFrame limpio.

### ETAPA 2 - EDA (Exploracion de Datos)

Objetivo: Ver como se relacionan los atributos con el valor del jugador.

### ETAPA 3 - FEATURE ENGINEERING

Objetivo: Transformar los datos en formato numerico para que el modelo los entienda.

### ETAPA 4 - ENTRENAMIENTO (Aprendizaje Supervisado: Regresion)

Objetivo: Entrenar un modelo que prediga el valor de mercado.

### ETAPA 5 - EVALUACION DEL MODELO

Objetivo: Medir la precision del modelo (aprendizaje supervisado tipo regresion).

### ETAPA 6 - DETECTAR JUGADORES INFRAVALORADOS

Objetivo: Calcular la diferencia entre valor real y predicho.

### ETAPA 7 - API (FastAPI)

Objetivo: Exponer el modelo como servicio.

### ETAPA 8 - DASHBOARD (Streamlit)

Objetivo: Interfaz visual interactiva con conexion al endpoint /predict de FastAPI para analizar nuevos jugadores.

---

## RESULTADO FINAL

El sistema completo incluira:

- Pipeline de limpieza y unificacion de datos
- Modelo de regresion supervisada entrenado y evaluado
- Sistema de deteccion automatica de jugadores infravalorados
- Dashboard interactivo para exploracion visual
- API REST para consultas y predicciones en tiempo real
