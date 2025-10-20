# 🎓 Seminario Complexivo - Grupo 7

**Autores:**  
📌 *Alberto Alexander Aldás Villacrés*  
📌 *Cristian Joel Riofrío Medina*  
📌 *Wilson Fernando Saavedra Álvarez*

---

## 🧠 Tema

**Predicción de Jugadores Infravalorados para Oportunidades de Negocio**

---

## 🎯 Objetivo General

Desarrollar un **sistema analítico integral** que permita **identificar jugadores de fútbol potencialmente infravalorados**, con base en su desempeño, características y evolución a lo largo del tiempo, generando información útil para la **toma de decisiones estratégicas y de negocio**.

---

## ⚙️ Objetivos Específicos

1. **Diseñar e implementar un pipeline de datos robusto**  
   - Integrar y limpiar múltiples fuentes (archivos Excel de FIFA 2015–2021)
   - Gestionar valores faltantes, duplicados y formatos inconsistentes
   - Normalizar variables numéricas y codificar variables categóricas

2. **Realizar un análisis exploratorio de datos (EDA)**  
   - Identificar patrones, tendencias y correlaciones entre rendimiento y valor de mercado
   - Detectar posibles casos de jugadores infravalorados

3. **Entrenar un modelo de Machine Learning (regresión)**  
   - Predecir el valor de mercado estimado de cada jugador a partir de variables como: edad, posición, potencial, calificación general y club
   - Evaluar el rendimiento del modelo mediante métricas como **MAE** y **R²**

4. **Desplegar el modelo como un servicio web (API)**  
   - Implementar una **API REST con FastAPI** para exponer las predicciones del modelo
   - Permitir la consulta dinámica de jugadores y valores estimados

5. **Visualizar los resultados en un dashboard interactivo**  
   - Integrar el modelo y los resultados en un **dashboard en Streamlit**, que permita explorar:
     - Ranking de jugadores infravalorados
     - Comparativas entre ligas, posiciones y temporadas
     - Evolución de valor y rendimiento individual

---

## 📁 Estructura del Proyecto

```
seminario-complexivo-grupo-7/
├── data/
│   └── dataset.xlsx                          # Dataset original FIFA 2015-2021
├── scripts/
│   ├── data_loader.py                        # Cargador de datos Excel
│   └── pipeline.py                           # Pipeline de limpieza y transformación
├── documentos/
│   ├── data_loader_documentacion.md          # Documentación técnica de data_loader
│   ├── pipeline_documentacion.md             # Documentación técnica de pipeline
│   
├── requirements.txt                          # Dependencias del proyecto
├── AGENTS.md                                 # Reglas de codificación
└── README.md                                 # Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar pipeline de datos

```bash
cd scripts
python pipeline.py
```

Esto generará el archivo `dataset_limpio.csv` con los datos procesados.

### 3. Explorar los datos

```python
import pandas as pd

df = pd.read_csv('dataset_limpio.csv')
print(df.head())
print(df.info())
```

---

## 📊 Estado del Proyecto

### ✅ Etapa 1 - Pipeline de Datos (Completada)

- [x] Cargar datos desde Excel (data_loader.py)
- [x] Unificar hojas 2015-2021 con columna `anio`
- [x] Renombrar columnas a nombres estandarizados en español
- [x] Limpiar filas inválidas y duplicados
- [x] Imputar valores faltantes
- [x] Generar dataset limpio (116,079 registros, 9 columnas, 0% nulos)

**Resultado:** `dataset_limpio.csv` con las siguientes columnas:
- `nombre` - Nombre del jugador
- `anio` - Temporada FIFA (2015-2021)
- `edad` - Edad del jugador
- `calificacion_general` - Habilidad general (0-99)
- `potencial` - Potencial futuro (0-99)
- `posicion` - Posición en el campo (GK, ST, CM, etc.)
- `club` - Club actual del jugador
- `nacionalidad` - Nacionalidad del jugador
- `valor_mercado` - Valor de mercado en euros

### 🔄 Próximas Etapas

- [ ] Etapa 2 - Análisis Exploratorio (EDA)
- [ ] Etapa 3 - Feature Engineering
- [ ] Etapa 4 - Entrenamiento del Modelo
- [ ] Etapa 5 - Evaluación del Modelo
- [ ] Etapa 6 - Detección de Infravalorados
- [ ] Etapa 7 - API REST (FastAPI)
- [ ] Etapa 8 - Dashboard (Streamlit)

---

## 📖 Documentación

Ver carpeta `/documentos/` para:

- **Documentación técnica de módulos:**
  - `data_loader_documentacion.md` - Cómo funciona el cargador de datos
  - `pipeline_documentacion.md` - Cómo funciona el pipeline de limpieza

- **Guías y reportes:**
  - `explicacion_detallada_pipeline.md` - Respuestas detalladas sobre cada paso
  - `reporte_etapa1_pipeline_datos.md` - Reporte completo de la Etapa 1
  - `resumen_mejoras_v2.md` - Historial de mejoras

---

## 🛠️ Tecnologías

- **Python 3.14** - Lenguaje principal
- **pandas 2.x** - Manipulación de datos
- **numpy 1.x** - Operaciones numéricas
- **openpyxl 3.x** - Lectura de archivos Excel
- **scikit-learn** - Machine Learning (próximamente)
- **FastAPI** - API REST (próximamente)
- **Streamlit** - Dashboard (próximamente)

---

## 📝 Calidad de Datos

**Dataset Final:**
- **Filas:** 116,079 jugadores (94.5% del dataset original)
- **Columnas:** 9 variables clave
- **Completitud:** 100% (0% valores nulos)
- **Duplicados:** 0 (eliminados 6,759 registros duplicados)
- **Periodo:** 2015-2021 (7 temporadas FIFA)

**Transformaciones Aplicadas:**
- Eliminación de 3 filas con edades inválidas
- Resolución de 6,759 duplicados (conservando mejor calidad)
- Imputación de 1,464 valores de club faltantes
- Reducción de 108 a 9 columnas (eliminando redundancia)

---

## 👥 Contribuciones

Este proyecto es desarrollado como parte del Seminario Complexivo de la carrera de Ingeniería de Software.

**Institución:** UNIANDES  
**Año Académico:** 2025  
**Zona Horaria:** America/Guayaquil

---

## 📄 Licencia

Este proyecto es de uso académico y educativo.

---