# 📊 DATOS - Sistema de Scouting FIFA

Repositorio de datos del proyecto: datasets originales, procesados y modelos de Machine Learning entrenados.

---

## 📁 Estructura de la Carpeta

```
datos/
│
├── 📁 originales/                    # Datos sin procesar
│   └── fifa.xlsx                     # Dataset original (7 hojas FIFA 15-21)
│
├── 📁 procesados/                    # Datos limpios y listos para ML
│   └── fifa_limpio.csv              # Dataset procesado (122,501 jugadores)
│
├── 📁 modelos/                       # Modelos ML entrenados
│   ├── modelo_fifa.joblib           # Random Forest (4000 árboles)
│   ├── encoder_fifa.joblib          # OneHotEncoder (categóricas)
│   └── club_encoding_fifa.joblib    # Encoding numérico de clubes
│
└── README.md                         # Este archivo
```

---

## 📂 Datos Originales

### `originales/fifa.xlsx`

**Descripción:**
- Dataset multi-hoja con datos históricos de jugadores FIFA
- Contiene 7 hojas (FIFA 15, 16, 17, 18, 19, 20, 21)
- Datos sin procesar del videojuego EA Sports FIFA

**Características:**
| Aspecto | Detalle |
|---------|---------|
| **Formato** | Excel (.xlsx) |
| **Hojas** | 7 (FIFA 15-21) |
| **Registros totales** | ~180,000 (antes de limpieza) |
| **Columnas por hoja** | 106 columnas |
| **Tamaño aproximado** | 40-50 MB |
| **Fuente** | Datos del videojuego FIFA |

**Columnas principales (inglés):**
- `sofifa_id` - ID único del jugador
- `short_name` - Nombre corto
- `long_name` - Nombre completo
- `age` - Edad
- `overall` - Valoración global
- `potential` - Potencial
- `value_eur` - Valor de mercado (EUR)
- `wage_eur` - Salario semanal (EUR)
- `club_name` - Club actual
- `league_name` - Liga
- `nationality_name` - Nacionalidad
- `player_positions` - Posiciones
- `pace`, `shooting`, `passing`, `dribbling`, `defending`, `physic` - Atributos
- ... y 85+ columnas adicionales

**⚠️ Nota importante:**
Este archivo **NO se incluye en el repositorio Git** (demasiado pesado). Se debe obtener por separado.

---

## 📊 Datos Procesados

### `procesados/fifa_limpio.csv`

**Descripción:**
- Dataset consolidado y limpio de las 7 hojas de Excel
- Listo para entrenamiento de modelos ML
- Columnas traducidas al español
- Valores normalizados y nulos imputados

**Características:**
| Aspecto | Detalle |
|---------|---------|
| **Formato** | CSV (delimitado por comas) |
| **Registros** | 122,501 jugadores únicos |
| **Columnas** | 73 columnas relevantes |
| **Tamaño aproximado** | 35-40 MB |
| **Encoding** | UTF-8 |

**Columnas principales (español):**
- `sofifa_id` - ID único
- `nombre_corto` - Nombre corto
- `nombre_completo` - Nombre completo
- `edad` - Edad (16-45)
- `overall` - Valoración global (40-100)
- `potencial` - Potencial (40-100)
- `valor_mercado_eur` - Valor de mercado en EUR (**target ML**)
- `salario_semanal_eur` - Salario semanal EUR
- `club` - Club actual (954 únicos)
- `liga` - Liga (39 únicas)
- `nacionalidad` - Nacionalidad (164 países)
- `posiciones_jugador` - Posiciones (27 únicas)
- `altura_cm` - Altura en cm
- `peso_kg` - Peso en kg
- `pie_preferido` - Pie preferido (Left/Right)
- `ritmo`, `tiro`, `pase`, `regate`, `defensa`, `fisico` - Atributos (0-100)
- `pie_debil` - Habilidad pie débil (1-5)
- `habilidades_regate` - Habilidad regate (1-5)
- `reputacion_internacional` - Reputación (1-5)
- `calidad_promedio` - Feature calculada (promedio atributos)
- `diferencia_potencial` - Feature calculada (potencial - overall)
- `categoria_edad` - Feature categórica (joven/consolidado/veterano)
- `categoria_posicion` - Feature categórica (delantero/medio/defensa/portero)
- `ratio_valor_salario` - Feature calculada (valor/salario)
- `anos_contrato_restantes` - Feature calculada
- `categoria_reputacion` - Feature categórica (baja/media/alta/estrella)

**Transformaciones aplicadas:**
1. ✅ Consolidación de 7 hojas en un DataFrame
2. ✅ Eliminación de duplicados (~57,500 eliminados)
3. ✅ Traducción de columnas a español
4. ✅ Eliminación de columnas con >70% nulos
5. ✅ Normalización de valores monetarios (K, M → EUR)
6. ✅ Normalización de fechas (ISO 8601)
7. ✅ Imputación de nulos por posición
8. ✅ Creación de 7 nuevas features
9. ✅ Selección de 73 columnas relevantes

**Estadísticas generales:**
```
Total jugadores: 122,501
Edad promedio: 25.3 años
Overall promedio: 66.2
Valor mercado promedio: €1,245,000
Países representados: 164
Clubes únicos: 954
Ligas únicas: 39
```

---

## 🤖 Modelos Entrenados

### `modelos/modelo_fifa.joblib`

**Descripción:**
- Modelo Random Forest Regressor entrenado
- Predice el valor de mercado de jugadores

**Características:**
| Aspecto | Detalle |
|---------|---------|
| **Formato** | joblib (pickle optimizado) |
| **Algoritmo** | Random Forest Regressor |
| **Estimadores** | 4000 árboles de decisión |
| **Profundidad** | max_depth=30 |
| **Features** | 84 (14 numéricas + 70 categóricas) |
| **Target** | `valor_mercado_eur` (log transformado) |
| **R² Score** | 0.65 - 0.98 (65-98%) |
| **Dataset Train** | 91,875 jugadores (75%) |
| **Dataset Test** | 30,626 jugadores (25%) |
| **Tamaño archivo** | ~500-800 MB |

**Hiperparámetros:**
```python
RandomForestRegressor(
    n_estimators=4000,
    max_depth=30,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features='sqrt',
    bootstrap=True,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
```

**Features numéricas utilizadas (14):**
1. `overall` - Valoración global
2. `potencial` - Potencial
3. `edad` - Edad
4. `altura_cm` - Altura
5. `peso_kg` - Peso
6. `ritmo` - Atributo ritmo
7. `tiro` - Atributo tiro
8. `pase` - Atributo pase
9. `regate` - Atributo regate
10. `defensa` - Atributo defensa
11. `fisico` - Atributo físico
12. `calidad_promedio` - Feature calculada
13. `diferencia_potencial` - Feature calculada
14. `ratio_valor_salario` - Feature calculada

**Features categóricas utilizadas (3 → 70 tras OneHotEncoding):**
1. `club` - 954 clubes únicos
2. `liga` - 39 ligas únicas
3. `posiciones_jugador` - 27 posiciones únicas
4. `nacionalidad` - 164 países
5. `pie_preferido` - 2 opciones
6. `categoria_edad` - 3 categorías

**Métricas de evaluación:**
- **R² Score:** 0.65 - 0.98
- **MAE:** Bajo (< 15% error relativo)
- **RMSE:** Bajo
- **OOB Score:** Similar a R² Test (indica robustez)

---

### `modelos/encoder_fifa.joblib`

**Descripción:**
- OneHotEncoder entrenado para variables categóricas
- Transforma categorías a formato numérico para el modelo

**Características:**
| Aspecto | Detalle |
|---------|---------|
| **Formato** | joblib |
| **Tipo** | scikit-learn OneHotEncoder |
| **Categorías únicas** | ~1,200 (total combinado) |
| **Output dimensions** | 70 columnas tras encoding |
| **Handle unknown** | 'ignore' (ignora categorías nuevas) |
| **Sparse output** | False (matriz densa) |
| **Tamaño archivo** | ~5-10 MB |

**Variables codificadas:**
- `liga` (39 únicas)
- `posiciones_jugador` (27 únicas)
- `nacionalidad` (164 únicas)
- `pie_preferido` (2 únicas)
- `categoria_edad` (3 únicas)

**Ejemplo de uso:**
```python
import joblib
encoder = joblib.load('datos/modelos/encoder_fifa.joblib')

# Datos categóricos de un jugador
categoricas = [['Spain Primera Division', 'ST', 'Argentina', 'Left', 'Joven']]

# Transformar a OneHot
encoded = encoder.transform(categoricas)
# Output: array con 70 columnas (0s y 1s)
```

---

### `modelos/club_encoding_fifa.joblib`

**Descripción:**
- Encoding numérico manual para clubes
- Mapea 954 clubes únicos a valores numéricos

**Características:**
| Aspecto | Detalle |
|---------|---------|
| **Formato** | joblib (diccionario Python) |
| **Tipo** | Dict[str, int] |
| **Clubes únicos** | 954 |
| **Rango valores** | 0 - 953 |
| **Tamaño archivo** | ~100-200 KB |

**Razón de existencia:**
Los clubes son demasiados (954) para OneHotEncoding eficiente, por eso se usa encoding numérico.

**Estructura:**
```python
{
    'Real Madrid': 0,
    'FC Barcelona': 1,
    'Manchester United': 2,
    'Liverpool': 3,
    ...
    'Unknown Club': 953
}
```

**Ejemplo de uso:**
```python
import joblib
club_encoding = joblib.load('datos/modelos/club_encoding_fifa.joblib')

# Codificar un club
club_code = club_encoding.get('Real Madrid', -1)
# Output: 0
```

---

## 🔄 Flujo de Datos

```
1. Dataset Original (fifa.xlsx)
   ├── 7 hojas (FIFA 15-21)
   └── ~180,000 registros × 106 columnas
          ↓
   [Pipeline de Limpieza]
   backend/pipeline_limpieza_datos.py
          ↓
2. Dataset Procesado (fifa_limpio.csv)
   ├── 122,501 jugadores × 73 columnas
   └── Listo para entrenamiento
          ↓
   [Entrenamiento ML]
   backend/entrenamiento.py
          ↓
3. Modelos Entrenados (modelos/*.joblib)
   ├── modelo_fifa.joblib (Random Forest)
   ├── encoder_fifa.joblib (OneHotEncoder)
   └── club_encoding_fifa.joblib (Dict clubes)
          ↓
   [Predicción en producción]
   backend/api_scouting_fifa.py
   frontend/dashboard_scouting_fifa.py
```

---

## 📦 Uso en Docker

La carpeta `datos/` se monta como **volumen externo** en los contenedores Docker:

```yaml
# docker-compose.yml
services:
  backend:
    volumes:
      - ../datos:/app/datos  # Datos externos
  
  frontend:
    volumes:
      - ../datos:/app/datos  # Mismo acceso
```

**Ventajas:**
- ✅ **No se reconstruyen** contenedores al actualizar datos
- ✅ **Persistencia** de datos entre reinicios
- ✅ **Compartidos** entre API y Dashboard
- ✅ **Imágenes ligeras** (solo código, no datos)

---

## 🔒 Seguridad y .gitignore

### Archivos excluidos de Git:

```gitignore
# .gitignore
datos/originales/*.xlsx          # Muy pesado (40-50 MB)
datos/procesados/*.csv           # Pesado (35-40 MB)
datos/modelos/*.joblib          # Muy pesado (500+ MB)
```

**Razones:**
- ❌ Archivos demasiado grandes para GitHub
- ❌ Se pueden regenerar con scripts
- ❌ Datos sensibles (si aplicara)

**¿Cómo compartir entonces?**
- Google Drive / Dropbox (link en README principal)
- Servidor FTP interno
- AWS S3 / Azure Blob Storage
- Git LFS (Large File Storage)

---

## 📊 Estadísticas de los Datos

### Dataset procesado:

| Métrica | Valor |
|---------|-------|
| **Total jugadores** | 122,501 |
| **Países únicos** | 164 |
| **Clubes únicos** | 954 |
| **Ligas únicas** | 39 |
| **Posiciones únicas** | 27 |
| **Rango de edad** | 16 - 45 años |
| **Rango overall** | 40 - 100 |
| **Rango potencial** | 40 - 100 |
| **Valor mercado min** | €0 |
| **Valor mercado max** | €100,000,000+ |
| **Valor mercado medio** | €1,245,000 |

### Top 5 ligas por valor total:

1. England Premier League
2. Spain Primera Division
3. Italy Serie A
4. Germany 1. Bundesliga
5. France Ligue 1

### Top 5 clubes por valor total:

1. Real Madrid
2. FC Barcelona
3. Manchester City
4. Paris Saint-Germain
5. Liverpool

---

## 🛠️ Regenerar Datos

### Si necesitas regenerar los archivos:

#### 1. Regenerar dataset procesado:

```powershell
# Asegúrate de tener fifa.xlsx en datos/originales/
cd backend
python pipeline_limpieza_datos.py
```

**Salida:** `datos/procesados/fifa_limpio.csv`

#### 2. Regenerar modelos ML:

```powershell
# Asegúrate de tener fifa_limpio.csv
cd backend
python entrenamiento.py
```

**Salida:** 3 archivos `.joblib` en `datos/modelos/`

---

## 📐 Tamaños Aproximados

| Archivo | Tamaño | Puede estar en Git? |
|---------|--------|---------------------|
| `fifa.xlsx` | 40-50 MB | ❌ No |
| `fifa_limpio.csv` | 35-40 MB | ❌ No |
| `modelo_fifa.joblib` | 500-800 MB | ❌ No |
| `encoder_fifa.joblib` | 5-10 MB | ❌ No |
| `club_encoding_fifa.joblib` | 100-200 KB | ⚠️ Tal vez |

**Total espacio en disco:** ~1 GB

---

## 🔍 Verificar Integridad de Datos

### Script de verificación:

```python
import pandas as pd
import joblib
import os

# Verificar que existan todos los archivos
archivos = {
    'Original': 'datos/originales/fifa.xlsx',
    'Procesado': 'datos/procesados/fifa_limpio.csv',
    'Modelo': 'datos/modelos/modelo_fifa.joblib',
    'Encoder': 'datos/modelos/encoder_fifa.joblib',
    'Club Encoding': 'datos/modelos/club_encoding_fifa.joblib'
}

for nombre, ruta in archivos.items():
    existe = os.path.exists(ruta)
    print(f"{nombre}: {'✅ Existe' if existe else '❌ No existe'}")

# Verificar datos procesados
if os.path.exists('datos/procesados/fifa_limpio.csv'):
    df = pd.read_csv('datos/procesados/fifa_limpio.csv')
    print(f"\nDataset: {len(df):,} jugadores × {len(df.columns)} columnas")
    print(f"Nulos: {df.isnull().sum().sum():,} valores")
```

---

## 📚 Documentación Relacionada

- **Pipeline de limpieza:** Ver `backend/scripts/limpieza/`
- **Entrenamiento ML:** Ver `backend/scripts/ml/`
- **Uso en API:** Ver `backend/api_scouting_fifa.py`
- **Uso en Dashboard:** Ver `frontend/dashboard_scouting_fifa.py`

---

## 👨‍💻 Mantenimiento

### Actualizar datos:

1. Obtener nueva versión de `fifa.xlsx`
2. Colocar en `datos/originales/`
3. Ejecutar pipeline de limpieza
4. Reentrenar modelos ML
5. Reiniciar API y Dashboard

### Backup recomendado:

```powershell
# Comprimir carpeta datos
Compress-Archive -Path datos/ -DestinationPath backup_datos_$(Get-Date -Format 'yyyyMMdd').zip
```

---

## ⚠️ Notas Importantes

1. **NO subir a Git:** Los archivos son demasiado grandes
2. **Mantener sincronizado:** Datos procesados y modelos deben corresponder
3. **Documentar cambios:** Si actualizas datos, documentar en CHANGELOG
4. **Verificar integridad:** Después de descargar datos, verificar checksums
5. **Espacio en disco:** Reservar al menos 2 GB para datos + cache

---

## 🎓 Uso Académico

**Proyecto:** Sistema de Scouting y Valoración FIFA  
**Asignatura:** Seminario Complexivo - Analítica con Python  
**Institución:** Universidad Regional Autónoma de los Andes (UniAndes)  
**Fecha:** Noviembre 2025

---

**📊 Datos listos para análisis y predicción de valor de mercado! ⚽🚀**
