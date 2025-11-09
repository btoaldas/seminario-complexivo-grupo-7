# 🔧 BACKEND - Sistema de Scouting FIFA

Sistema de procesamiento de datos, entrenamiento de modelos ML y API REST para predicción de valor de mercado de jugadores de fútbol.

---

## 📁 Estructura del Backend

```
backend/
│
├── 📄 pipeline_limpieza_datos.py        # Pipeline completo de limpieza
├── 📄 entrenamiento.py                  # Entrenamiento de modelos ML
├── 📄 api_scouting_fifa.py             # API REST (FastAPI)
│
├── 📁 scripts/
│   ├── limpieza/                        # 6 módulos de procesamiento
│   │   ├── cargador_datos.py          # Carga multi-hoja Excel
│   │   ├── renombrado_columnas.py     # Traducción a español
│   │   ├── limpieza_datos.py          # Eliminación duplicados/nulos
│   │   ├── imputacion_datos.py        # Imputación por posición
│   │   ├── nuevas_caracteristicas.py  # Ingeniería de features
│   │   └── guardado_datos.py          # Exportación CSV
│   │
│   └── ml/                              # 3 módulos de Machine Learning
│       ├── preprocesamiento_modelo.py  # Selección/encoding features
│       ├── entrenamiento_modelo.py     # Training y evaluación
│       └── guardado_modelo.py          # Persistencia .joblib
│
├── 📁 pruebas/                          # Scripts de testing
│   ├── probar_api.py                   # Test endpoints API
│   ├── verificar_datos_api.py          # Verificación datos
│   └── analisis_error_modelo.py        # Análisis errores ML
│
├── requirements-api.txt                 # Dependencias API
└── README.md                            # Este archivo
```

---

## 🚀 Inicio Rápido

### 1️⃣ Ejecutar Pipeline de Limpieza

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ir a carpeta backend
cd backend

# Ejecutar pipeline
python pipeline_limpieza_datos.py
```

**📤 Salida generada:**
- `datos/procesados/fifa_limpio.csv` (122,501 jugadores × 73 columnas)

---

### 2️⃣ Entrenar Modelos de Machine Learning

```powershell
# Desde carpeta backend (con venv activado)
python entrenamiento.py
```

**📤 Modelos generados en `datos/modelos/`:**
- `modelo_fifa.joblib` - Random Forest (R² = **0.98+**)
- `encoder_fifa.joblib` - OneHotEncoder para categóricas
- `club_encoding_fifa.joblib` - Encoding de clubes

**🤖 Modelos entrenados:**
1. **Regresión Lineal** (baseline) → R² ~0.35-0.40
2. **Random Forest** (ganador) → R² ~0.65-0.98

**🏆 Modelo seleccionado:** Random Forest con 4000 estimadores

---

### 3️⃣ Iniciar API REST

```powershell
# Opción A: Ejecutar directamente
cd backend
python api_scouting_fifa.py

# Opción B: Con uvicorn (recomendado para desarrollo)
uvicorn api_scouting_fifa:app --reload --host 0.0.0.0 --port 8000
```

**⚠️ IMPORTANTE:** La primera carga tarda 30-60 segundos (carga 4000 árboles + 122K jugadores)

**🌐 Servicios disponibles:**
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs

---

### 4️⃣ Verificar que funciona

Abre en el navegador: **http://localhost:8000**

Deberías ver un JSON con información de la API.

---

## 🧪 Probar el Sistema

### Probar API con Scripts de Prueba

**En otra terminal** (mientras la API está corriendo):

```powershell
# Test completo de endpoints
cd backend/pruebas
python probar_api.py

# Verificar datos de la API
python verificar_datos_api.py

# Analizar errores del modelo
python analisis_error_modelo.py
```

---

## 📊 Pipeline de Limpieza de Datos

### Proceso completo (7 etapas):

1. **Carga de datos** (`cargador_datos.py`)
   - Lee archivo Excel multi-hoja (FIFA 15-21)
   - Consolida 7 hojas en un DataFrame único
   - Total: 122,501 jugadores

2. **Renombrado de columnas** (`renombrado_columnas.py`)
   - Traduce 106 columnas de inglés a español
   - Normaliza nombres (snake_case)

3. **Limpieza básica** (`limpieza_datos.py`)
   - Elimina duplicados
   - Elimina columnas con >70% valores nulos
   - Normaliza valores monetarios (K, M → EUR)
   - Normaliza fechas (ISO 8601)

4. **Selección de columnas** (`limpieza_datos.py`)
   - Selecciona 73 columnas relevantes
   - Descarta columnas redundantes

5. **Imputación de nulos** (`imputacion_datos.py`)
   - Imputación inteligente por posición
   - Porteros: atributos defensivos
   - Delanteros: atributos ofensivos
   - etc.

6. **Ingeniería de features** (`nuevas_caracteristicas.py`)
   - Crea 7 nuevas características:
     - `calidad_promedio`
     - `diferencia_potencial`
     - `categoria_edad`
     - `categoria_posicion`
     - `ratio_valor_salario`
     - `anos_contrato_restantes`
     - `categoria_reputacion`

7. **Guardado** (`guardado_datos.py`)
   - Exporta CSV limpio
   - Ubicación: `datos/procesados/fifa_limpio.csv`

---

## 🤖 Entrenamiento de Modelos ML

### Configuración del modelo Random Forest:

```python
RandomForestRegressor(
    n_estimators=4000,      # 4000 árboles de decisión
    max_depth=30,           # Profundidad máxima 30
    min_samples_split=10,   # Mínimo 10 muestras para split
    min_samples_leaf=4,     # Mínimo 4 muestras por hoja
    max_features='sqrt',    # sqrt(84) ≈ 9 features por split
    bootstrap=True,         # Bootstrap habilitado
    oob_score=True,         # Validación OOB
    n_jobs=-1,              # Todos los cores CPU
    random_state=42
)
```

### Features utilizadas (84 totales):

**Numéricas (14):**
- overall, potencial, edad, altura_cm, peso_kg
- ritmo, tiro, pase, regate, defensa, fisico
- calidad_promedio, diferencia_potencial, ratio_valor_salario

**Categóricas (70 tras OneHotEncoding):**
- club (954 únicos) → encoding numérico
- liga (39 únicas)
- posicion (27 únicas)
- nacionalidad (164 únicas)
- pie_preferido (2 opciones)
- categoria_edad (3 categorías)

### Métricas del modelo:

| Modelo | R² Score | MAE | RMSE | Seleccionado |
|--------|----------|-----|------|--------------|
| Regresión Lineal | ~0.35-0.40 | Alto | Alto | ❌ |
| **Random Forest** | **0.65-0.98** | Bajo | Bajo | ✅ |

**🎯 Interpretación:**
- R² = 0.98 significa que el modelo explica el **98%** de la variabilidad del valor de mercado
- El modelo considera club, liga, reputación y atributos técnicos
- Error promedio: < 15% del valor real

---

## 🌐 API REST - Endpoints

### Documentación interactiva:
👉 http://localhost:8000/docs

### Endpoints disponibles:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Info de la API |
| `/docs` | GET | Documentación Swagger |
| `/jugadores/filtros` | GET | Filtros disponibles |
| `/jugadores/buscar` | GET | Buscar jugadores |
| `/jugadores/{id}/perfil` | GET | Perfil de jugador |
| `/ml/predecir_valor` | POST | **Predicción ML** |
| `/jugadores/infravalorados` | GET | Top infravalorados |
| `/jugadores/sobrevalorados` | GET | Top sobrevalorados |
| `/eda/estadisticas_generales` | GET | KPIs del dataset |
| `/eda/datos_graficos` | GET | Datos para gráficos |

---

## 💡 Ejemplos de Uso de la API

### Ejemplo 1: Buscar los 10 jugadores más valiosos

```bash
GET http://localhost:8000/jugadores/buscar?limite=10&ordenar_por=valor_mercado_eur&orden_descendente=true
```

### Ejemplo 2: Buscar delanteros jóvenes prometedores

```bash
GET http://localhost:8000/jugadores/buscar?categoria_posicion=Delantero&edad_min=18&edad_max=23&potencial_min=80&limite=20
```

### Ejemplo 3: Ver perfil completo de un jugador

```bash
GET http://localhost:8000/jugadores/158023/perfil
```

### Ejemplo 4: Predecir valor de mercado (POST con Python)

```python
import requests

url = "http://localhost:8000/ml/predecir_valor"
datos = {
    "edad": 22,
    "valoracion_global": 78,
    "potencial": 85,
    "ritmo_velocidad": 88,
    "tiro_disparo": 72,
    "pase": 70,
    "club": "Real Madrid",
    "liga": "Spain Primera Division",
    "posiciones_jugador": "LW",
    "nacionalidad": "Argentina",
    "reputacion_internacional": 4
}

response = requests.post(url, json=datos)
resultado = response.json()

print(f"Valor predicho: €{resultado['valor_predicho_eur']:,.0f}")
print(f"Confianza: {resultado['confianza_prediccion']}")
```

### Ejemplo 5: Top jugadores infravalorados

```bash
GET http://localhost:8000/jugadores/infravalorados?top=20&diferencia_minima_porcentual=30&edad_maxima=25
```

**Respuesta:**
```json
{
  "total_encontrados": 20,
  "jugadores": [
    {
      "nombre": "K. Mbappé",
      "edad": 21,
      "overall": 90,
      "potencial": 95,
      "valor_real_eur": 180000000,
      "valor_predicho_eur": 250000000,
      "diferencia_eur": 70000000,
      "diferencia_porcentual": 38.89,
      "club": "Paris Saint-Germain"
    }
  ]
}
```

---

## 📈 Características del Modelo ML

### Modelo Ganador: **Random Forest Regressor**

| Característica | Valor |
|----------------|-------|
| **Tipo** | Random Forest (Ensemble) |
| **Estimadores** | 4000 árboles |
| **Profundidad** | max_depth=30 |
| **R² Score** | 0.65 - 0.98 (65-98%) |
| **Features** | 84 (14 numéricas + 70 categóricas) |
| **Dataset Training** | 91,875 jugadores |
| **Dataset Test** | 30,626 jugadores |
| **Error promedio** | < 15% del valor real |

### ¿Por qué Random Forest ganó?

✅ **Ventajas sobre Regresión Lineal:**
- Captura relaciones no lineales
- Maneja mejor interacciones entre variables (club × liga × atributos)
- Robusto ante outliers
- No requiere normalización
- OOB Score integrado para validación

### Archivos del modelo (ubicados en `datos/modelos/`):

```
datos/modelos/
├── modelo_fifa.joblib           # Random Forest entrenado (4000 árboles)
├── encoder_fifa.joblib          # OneHotEncoder para categóricas
└── club_encoding_fifa.joblib    # Encoding numérico de clubes
```

---

## 🛠️ Solución de Problemas

### ❌ La API no inicia

**Verificar:**
1. ✅ Estás en el directorio `backend`
2. ✅ Entorno virtual activado (`venv`)
3. ✅ Existen los archivos del modelo en `datos/modelos/`:
   - `modelo_fifa.joblib`
   - `encoder_fifa.joblib`
   - `club_encoding_fifa.joblib`

**Solución:**
```powershell
# Entrenar modelo si no existe
cd backend
python entrenamiento.py
```

---

### ❌ Error "ModuleNotFoundError"

**Solución:**
```powershell
# Instalar dependencias de la API
pip install -r backend/requirements-api.txt
```

---

### ⏳ La API tarda mucho en cargar (30-60 segundos)

**Es normal.** El modelo tiene:
- 4000 árboles de decisión
- 122,501 jugadores en memoria
- 3 archivos .joblib (modelo + encoders)

**Primera carga:** 30-60 segundos  
**Siguientes peticiones:** < 100ms

---

### ❌ Puerto 8000 ya en uso

**Solución Windows PowerShell:**
```powershell
# Matar proceso Python que usa el puerto
Get-Process python | Where-Object {$_.Path -like '*python*'} | Stop-Process -Force

# Reiniciar API
cd backend
python api_scouting_fifa.py
```

**Solución alternativa (cambiar puerto):**
```powershell
uvicorn api_scouting_fifa:app --port 8001
```

---

### ❌ Error al cargar modelo "FileNotFoundError"

**Causa:** Archivos del modelo no existen en `datos/modelos/`

**Solución:**
```powershell
# Entrenar modelo nuevamente
cd backend
python entrenamiento.py
```

---

## 📚 Estructura de Datos

### Dataset procesado (`datos/procesados/fifa_limpio.csv`):

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `sofifa_id` | int | ID único del jugador |
| `nombre_completo` | str | Nombre del jugador |
| `edad` | int | Edad (16-45) |
| `overall` | int | Valoración global (40-100) |
| `potencial` | int | Potencial (40-100) |
| `valor_mercado_eur` | float | Valor de mercado en EUR (**target**) |
| `club` | str | Club actual |
| `liga` | str | Liga donde juega |
| `nacionalidad` | str | Nacionalidad |
| `posiciones_jugador` | str | Posición(es) |
| ... | ... | +63 columnas adicionales |

---

## 🎯 Próximos Pasos

✅ **Completado:**
1. ✅ Pipeline de limpieza de datos
2. ✅ Entrenamiento de modelos ML
3. ✅ API REST funcional

🚧 **Pendiente:**
4. Dashboard interactivo (Streamlit) → Ver `frontend/`
5. Documentación completa de API
6. Despliegue en Docker

---

## 👨‍💻 Uso Interno

Este README está orientado a desarrolladores del backend.  
Para documentación de usuario final, ver: `README.md` (raíz del proyecto)
