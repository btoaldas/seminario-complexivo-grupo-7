# 📘 Documentación Técnica - data_loader.py

**Módulo:** `scripts/data_loader.py`  
**Versión:** 1.0  
**Fecha:** 19 de octubre de 2025  
**Autor:** Grupo 7 - Seminario Complexivo

---

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Propósito y Responsabilidad](#propósito-y-responsabilidad)
3. [Dependencias](#dependencias)
4. [Arquitectura del Módulo](#arquitectura-del-módulo)
5. [Funciones Detalladas](#funciones-detalladas)
6. [Flujo de Ejecución](#flujo-de-ejecución)
7. [Manejo de Errores](#manejo-de-errores)
8. [Ejemplos de Uso](#ejemplos-de-uso)
9. [Salidas y Resultados](#salidas-y-resultados)

---

## 📖 Descripción General

`data_loader.py` es el módulo encargado de **cargar y leer** el archivo Excel del dataset FIFA 15-21. Actúa como una **capa de abstracción** entre el archivo físico y el resto del sistema, proporcionando funciones reutilizables para acceder a los datos.

### Características principales:
- ✅ Carga completa del archivo Excel (todas las hojas)
- ✅ Carga individual de hojas específicas
- ✅ Detección automática de rutas del dataset
- ✅ Manejo robusto de errores
- ✅ Validación de existencia de archivos y hojas
- ✅ Reportes informativos de carga

---

## 🎯 Propósito y Responsabilidad

### ¿Qué hace este módulo?

**Función principal:** Leer el archivo `data/dataset.xlsx` y convertir sus hojas en DataFrames de pandas.

### ¿Qué NO hace?

- ❌ No limpia ni transforma datos (eso lo hace `pipeline.py`)
- ❌ No valida el contenido de los datos
- ❌ No modifica el archivo original
- ❌ No guarda datos procesados

### Principio de diseño:

**Single Responsibility Principle (SRP):** Este módulo tiene una sola responsabilidad: **leer datos de Excel**.

---

## 📦 Dependencias

```python
import pandas as pd      # Lectura de archivos Excel y manejo de DataFrames
import os               # Manipulación de rutas de archivos
from typing import Dict, Optional  # Type hints para mejor documentación
```

### Librerías externas requeridas:
- **pandas >= 2.0**: Para lectura de Excel y DataFrames
- **openpyxl >= 3.0**: Backend de pandas para archivos .xlsx

---

## 🏗️ Arquitectura del Módulo

```
data_loader.py
│
├── [CONFIGURACIÓN]
│   ├── directorio_script  → Ruta absoluta del script actual
│   └── ruta_dataset       → Ruta al archivo dataset.xlsx
│
├── [FUNCIONES PÚBLICAS]
│   ├── cargar_excel_completo()       → Carga todas las hojas
│   ├── cargar_hoja_individual()      → Carga una hoja específica
│   └── obtener_ruta_dataset()        → Retorna ruta absoluta del dataset
│
└── [BLOQUE DE PRUEBA]
    └── if __name__ == "__main__":    → Pruebas cuando se ejecuta directo
```

---

## 🔧 Funciones Detalladas

### 1. `cargar_excel_completo(ruta: Optional[str] = None) -> Dict[str, pd.DataFrame]`

**Propósito:** Cargar todas las hojas del archivo Excel en un solo diccionario.

#### Parámetros:
| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `ruta` | `Optional[str]` | Ruta personalizada al archivo Excel | `None` (usa ruta por defecto) |

#### Retorno:
- **Tipo:** `Dict[str, pd.DataFrame]` o `None`
- **Estructura:** `{"nombre_hoja": DataFrame, ...}`
- **Ejemplo:**
  ```python
  {
      "fifa15": DataFrame(...),
      "fifa16": DataFrame(...),
      ...
      "fifa21": DataFrame(...)
  }
  ```

#### ¿Cómo funciona?

```python
def cargar_excel_completo(ruta: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    # 1. Determinar ruta del archivo
    ruta_archivo = ruta if ruta else ruta_dataset
    
    # 2. Intentar cargar Excel
    try:
        # pd.read_excel con sheet_name=None lee TODAS las hojas
        hojas = pd.read_excel(ruta_archivo, sheet_name=None)
        
        # 3. Mostrar resumen de cada hoja
        for nombre_hoja, df in hojas.items():
            print(f"  - hoja '{nombre_hoja}': {df.shape[0]} filas, {df.shape[1]} columnas")
        
        return hojas
    
    except FileNotFoundError:
        # Archivo no existe
        print(f"error: el archivo no se encontró en: {ruta_archivo}")
        return None
    
    except Exception as e:
        # Cualquier otro error
        print(f"error al cargar los datos: {e}")
        return None
```

#### Proceso paso a paso:

1. **Validar ruta:** Usa ruta personalizada o ruta por defecto
2. **Lectura masiva:** `pd.read_excel(..., sheet_name=None)` carga todas las hojas
3. **Reporte:** Muestra estadísticas de cada hoja (filas x columnas)
4. **Retorno:** Diccionario con todas las hojas o `None` si hay error

#### Salida en consola:

```
cargando todas las hojas desde: C:\...\data\dataset.xlsx
datos cargados exitosamente: 7 hojas encontradas
  - hoja 'fifa15': 17,588 filas, 108 columnas
  - hoja 'fifa16': 17,954 filas, 108 columnas
  - hoja 'fifa17': 17,981 filas, 108 columnas
  - hoja 'fifa18': 18,207 filas, 108 columnas
  - hoja 'fifa19': 18,278 filas, 108 columnas
  - hoja 'fifa20': 18,278 filas, 108 columnas
  - hoja 'fifa21': 18,944 filas, 108 columnas
```

---

### 2. `cargar_hoja_individual(nombre_hoja: str, ruta: Optional[str] = None) -> Optional[pd.DataFrame]`

**Propósito:** Cargar una hoja específica del Excel (útil para pruebas o análisis parciales).

#### Parámetros:
| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `nombre_hoja` | `str` | Nombre exacto de la hoja a cargar | `"fifa21"` |
| `ruta` | `Optional[str]` | Ruta personalizada al archivo | `None` |

#### Retorno:
- **Tipo:** `pd.DataFrame` o `None`
- **Contenido:** DataFrame con los datos de la hoja seleccionada

#### ¿Cómo funciona?

```python
def cargar_hoja_individual(nombre_hoja: str, ruta: Optional[str] = None) -> Optional[pd.DataFrame]:
    # 1. Determinar ruta
    ruta_archivo = ruta if ruta else ruta_dataset
    
    # 2. Intentar cargar hoja específica
    try:
        df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
        print(f"hoja cargada exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    
    except ValueError:
        # La hoja no existe en el archivo
        print(f"error: la hoja '{nombre_hoja}' no existe en el archivo.")
        return None
    
    except FileNotFoundError:
        # Archivo no existe
        print(f"error: el archivo no se encontró en: {ruta_archivo}")
        return None
    
    except Exception as e:
        # Cualquier otro error
        print(f"error al cargar la hoja: {e}")
        return None
```

#### Casos de uso:

1. **Desarrollo/Testing:** Cargar solo una hoja para pruebas rápidas
2. **Análisis parcial:** Analizar una temporada específica
3. **Debugging:** Verificar contenido de una hoja particular

#### Ejemplo:

```python
# Cargar solo FIFA 21
df_21 = cargar_hoja_individual("fifa21")
if df_21 is not None:
    print(df_21.head())
```

---

### 3. `obtener_ruta_dataset() -> str`

**Propósito:** Retornar la ruta absoluta del dataset (útil para debugging y logging).

#### Retorno:
- **Tipo:** `str`
- **Ejemplo:** `"C:/proyectos/seminario-complexivo-grupo-7/data/dataset.xlsx"`

#### ¿Cómo funciona?

```python
def obtener_ruta_dataset() -> str:
    """
    Retorna la ruta absoluta del archivo dataset.xlsx.
    """
    return os.path.abspath(ruta_dataset)
```

#### Uso:

```python
print(f"Dataset ubicado en: {obtener_ruta_dataset()}")
# Output: Dataset ubicado en: C:/proyectos/.../data/dataset.xlsx
```

---

## 🔄 Flujo de Ejecución

### Escenario 1: Ejecución desde otro módulo (pipeline.py)

```python
# En pipeline.py
from data_loader import cargar_excel_completo

# Cargar todas las hojas
hojas = cargar_excel_completo()

# Procesar cada hoja
for nombre, df in hojas.items():
    # ... procesamiento ...
```

### Escenario 2: Ejecución directa (testing)

```bash
$ python data_loader.py
```

**Salida:**
```
=== prueba de cargador de datos fifa ===

directorio del script: C:\...\scripts\data_loader.py
ruta del dataset: C:\...\data\dataset.xlsx

cargando todas las hojas desde: C:\...\data\dataset.xlsx
datos cargados exitosamente: 7 hojas encontradas
  - hoja 'fifa15': 17,588 filas, 108 columnas
  ...

=== muestra de la hoja 'fifa15' ===
   short_name  age  overall  potential  ...
0  L. Messi    28      94        94     ...
...

=== información de la hoja 'fifa15' ===
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 17588 entries, 0 to 17587
Columns: 108 entries, short_name to gk_speed
dtypes: float64(88), int64(10), object(10)
```

---

## ⚠️ Manejo de Errores

### Errores capturados:

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError` | Archivo `dataset.xlsx` no existe | Verificar que el archivo esté en `data/` |
| `ValueError` | Hoja solicitada no existe en el Excel | Verificar nombre exacto de la hoja |
| `ImportError` | Falta librería `openpyxl` | Ejecutar `pip install openpyxl` |
| `PermissionError` | Archivo abierto en Excel | Cerrar el archivo Excel |

### Diseño de error handling:

```python
try:
    # Intentar operación
    hojas = pd.read_excel(...)
    return hojas
    
except FileNotFoundError:
    # Error específico: archivo no existe
    print("error: el archivo no se encontró...")
    return None
    
except Exception as e:
    # Error genérico: cualquier otra cosa
    print(f"error al cargar los datos: {e}")
    return None
```

**Principio:** Siempre retornar `None` en caso de error (nunca lanzar excepciones sin manejar).

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Cargar todas las hojas

```python
from data_loader import cargar_excel_completo

# Cargar todo el dataset
hojas = cargar_excel_completo()

if hojas is not None:
    print(f"Total de hojas: {len(hojas)}")
    print(f"Nombres: {list(hojas.keys())}")
    
    # Acceder a una hoja específica
    df_fifa21 = hojas['fifa21']
    print(df_fifa21.shape)  # (18944, 108)
```

### Ejemplo 2: Cargar hoja individual

```python
from data_loader import cargar_hoja_individual

# Cargar solo FIFA 21
df = cargar_hoja_individual("fifa21")

if df is not None:
    print(f"Jugadores en FIFA 21: {len(df)}")
    print(df.columns.tolist())  # Lista de columnas
```

### Ejemplo 3: Verificar ruta del dataset

```python
from data_loader import obtener_ruta_dataset
import os

ruta = obtener_ruta_dataset()
print(f"Dataset: {ruta}")
print(f"¿Existe? {os.path.exists(ruta)}")
```

### Ejemplo 4: Usar ruta personalizada

```python
from data_loader import cargar_excel_completo

# Cargar desde otra ubicación
hojas = cargar_excel_completo(ruta="C:/otro/dataset.xlsx")
```

---

## 📤 Salidas y Resultados

### ¿Qué retorna cada función?

#### `cargar_excel_completo()`
```python
{
    "fifa15": DataFrame(17588 rows × 108 columns),
    "fifa16": DataFrame(17954 rows × 108 columns),
    "fifa17": DataFrame(17981 rows × 108 columns),
    "fifa18": DataFrame(18207 rows × 108 columns),
    "fifa19": DataFrame(18278 rows × 108 columns),
    "fifa20": DataFrame(18278 rows × 108 columns),
    "fifa21": DataFrame(18944 rows × 108 columns)
}
```

**Total registros:** 127,230 filas (antes de limpieza)  
**Columnas por hoja:** 108 (todas las hojas tienen la misma estructura)

#### `cargar_hoja_individual("fifa21")`
```python
DataFrame(18944 rows × 108 columns)

Columnas incluidas:
- short_name, age, overall, potential, value_eur, wage_eur
- club_name, nationality, player_positions
- pace, shooting, passing, dribbling, defending, physical
- ... y 96 columnas más
```

#### `obtener_ruta_dataset()`
```python
"C:/proyectos/seminario-complexivo-grupo-7/data/dataset.xlsx"
```

---

## 📊 Estadísticas del Dataset

### Tamaño del archivo:
- **Formato:** .xlsx (Excel)
- **Tamaño:** ~50 MB
- **Hojas:** 7 (fifa15 a fifa21)
- **Registros totales:** 127,230 jugadores
- **Columnas:** 108 atributos por jugador

### Distribución por año:

| Año | Hoja | Jugadores |
|-----|------|-----------|
| 2015 | fifa15 | 17,588 |
| 2016 | fifa16 | 17,954 |
| 2017 | fifa17 | 17,981 |
| 2018 | fifa18 | 18,207 |
| 2019 | fifa19 | 18,278 |
| 2020 | fifa20 | 18,278 |
| 2021 | fifa21 | 18,944 |
| **Total** | - | **127,230** |

---

## 🔍 Validaciones Implementadas

### Validación 1: Existencia del archivo
```python
except FileNotFoundError:
    print(f"error: el archivo no se encontró en: {ruta_archivo}")
    return None
```

### Validación 2: Existencia de la hoja
```python
except ValueError:
    print(f"error: la hoja '{nombre_hoja}' no existe en el archivo.")
    return None
```

### Validación 3: Permisos de lectura
```python
except Exception as e:
    print(f"error al cargar los datos: {e}")
    return None
```

---

## 📝 Convenciones de Código

Según `AGENTS.md`:

- ✅ **snake_case:** Todas las variables y funciones (`cargar_excel_completo`, `ruta_dataset`)
- ✅ **Sin tildes en código:** `directorio_script`, no `directorio_script`
- ✅ **Tildes en comentarios:** "Carga todas las hojas del archivo Excel"
- ✅ **Type hints:** Todas las funciones tienen anotaciones de tipo
- ✅ **Docstrings:** Todas las funciones documentadas

---

## 🎯 Resumen Ejecutivo

### ¿Qué hace `data_loader.py`?
Carga archivos Excel del dataset FIFA y los convierte en DataFrames de pandas.

### ¿Cómo lo hace?
Usando `pd.read_excel()` con manejo robusto de errores y validaciones.

### ¿Qué produce?
Diccionarios con todas las hojas o DataFrames individuales listos para ser procesados por `pipeline.py`.

### Características clave:
- ✅ Simple y enfocado (una sola responsabilidad)
- ✅ Robusto (maneja todos los errores posibles)
- ✅ Reutilizable (funciones independientes)
- ✅ Documentado (type hints y docstrings)
- ✅ Testeable (bloque `if __name__ == "__main__"`)

---

**Fin de la documentación técnica**  
**Última actualización:** 19 de octubre de 2025
