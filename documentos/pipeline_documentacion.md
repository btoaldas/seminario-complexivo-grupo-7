# 📘 Documentación Técnica - pipeline.py

**Módulo:** `scripts/pipeline.py`  
**Versión:** 2.0  
**Fecha:** 19 de octubre de 2025  
**Autor:** Grupo 7 - Seminario Complexivo

---

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Propósito y Responsabilidad](#propósito-y-responsabilidad)
3. [Arquitectura del Pipeline](#arquitectura-del-pipeline)
4. [Parámetros y Configuración](#parámetros-y-configuración)
5. [Funciones del Pipeline](#funciones-del-pipeline)
6. [Flujo Completo de Ejecución](#flujo-completo-de-ejecución)
7. [Transformaciones Aplicadas](#transformaciones-aplicadas)
8. [Reportes y Ejemplos](#reportes-y-ejemplos)
9. [Salidas y Resultados](#salidas-y-resultados)
10. [Manejo de Errores](#manejo-de-errores)

---

## 📖 Descripción General

`pipeline.py` es el **motor de limpieza y transformación de datos** del proyecto. Toma el dataset crudo de FIFA (122,841 registros, 108 columnas) y lo convierte en un dataset limpio y listo para Machine Learning (116,079 registros, 9 columnas).

### Características principales:
- ✅ Pipeline completo de 10 pasos automatizados
- ✅ Reportes detallados con ejemplos concretos
- ✅ Manejo robusto de valores faltantes y duplicados
- ✅ Validación de rangos y eliminación de anomalías
- ✅ Selección inteligente de features para ML
- ✅ Generación de CSV final listo para modelado

---

## 🎯 Propósito y Responsabilidad

### ¿Qué hace este módulo?

**Función principal:** Transformar datos crudos en datos limpios y estructurados para Machine Learning.

### Pipeline de 10 pasos:

1. **Cargar datos** - Lee todas las hojas Excel
2. **Renombrar columnas** - Traduce nombres al español
3. **Limpieza básica** - Elimina filas inválidas
4. **Procesar valores monetarios** - Convierte a float
5. **Resolver duplicados** - Elimina registros duplicados
6. **Imputar valores** - Rellena valores faltantes
7. **Filtrar sin objetivo** - Elimina sin valor_mercado
8. **Seleccionar columnas** - Reduce de 108 a 9 columnas
9. **Generar reporte** - Estadísticas de calidad
10. **Guardar CSV** - Exporta dataset limpio

---

## 🏗️ Arquitectura del Pipeline

```
pipeline.py
│
├── [PARÁMETROS GLOBALES]
│   ├── posiciones_validas        → Set de posiciones FIFA válidas
│   ├── ratio_nulos_eliminar      → Umbral de nulos (90%)
│   ├── rango_edad               → (14, 45) años
│   ├── rango_overall            → (30, 99) puntos
│   ├── rango_potential          → (30, 99) puntos
│   └── mapeo_columnas           → Diccionario inglés→español
│
├── [UTILIDADES]
│   ├── imprimir_reporte_paso()           → Reporte visual de cada paso
│   ├── leer_todas_hojas_con_anio()       → Carga y agrega columna año
│   ├── inferir_anio_desde_nombre_hoja()  → Extrae año del nombre
│   ├── renombrar_columnas_dataset()      → Aplica mapeo de columnas
│   └── convertir_dinero_a_numero()       → Convierte valores monetarios
│
├── [FUNCIONES DE LIMPIEZA]
│   ├── eliminar_filas_resumen_y_fuera_rango()  → Paso 3
│   ├── agregar_columnas_dinero_numericas()     → Paso 4
│   ├── eliminar_y_resolver_duplicados()        → Paso 5
│   ├── imputar_y_llenar()                      → Paso 6
│   ├── eliminar_filas_sin_objetivo()           → Paso 7
│   └── seleccionar_columnas_para_ml()          → Paso 8
│
├── [ORQUESTADOR]
│   └── ejecutar_pipeline()              → Ejecuta todo el flujo
│
└── [PUNTO DE ENTRADA]
    └── if __name__ == "__main__":       → Ejecución principal
```

---

## ⚙️ Parámetros y Configuración

### 1. Posiciones válidas de jugadores

```python
posiciones_validas = {
    "GK",      # Goalkeeper (Portero)
    "CB",      # Center Back (Defensa central)
    "LB", "RB",  # Left/Right Back (Lateral izquierdo/derecho)
    "LWB", "RWB",  # Left/Right Wing Back (Carrilero)
    "CDM",     # Central Defensive Midfielder (Pivote)
    "CM",      # Central Midfielder (Mediocentro)
    "CAM",     # Central Attacking Midfielder (Mediapunta)
    "LM", "RM",  # Left/Right Midfielder (Mediocentro lateral)
    "LW", "RW",  # Left/Right Winger (Extremo)
    "ST",      # Striker (Delantero)
    "CF"       # Center Forward (Delantero centro)
}
```

**Propósito:** Validar que las posiciones sean coherentes con el fútbol profesional.

### 2. Umbral de nulos

```python
ratio_nulos_eliminar = 0.90  # 90%
```

**Criterio:** Si una fila tiene más del 90% de sus columnas vacías, se descarta.

**Ejemplo:**
- Fila con 100 columnas y 91 vacías → **ELIMINAR** (91% > 90%)
- Fila con 100 columnas y 50 vacías → **CONSERVAR** (50% < 90%)

### 3. Rangos válidos

```python
rango_edad = (14, 45)        # 14 a 45 años
rango_overall = (30, 99)     # Calificación general: 30-99
rango_potential = (30, 99)   # Potencial: 30-99
```

**Justificación:**
- **Edad:** Jugadores profesionales entre 14 años (juveniles) y 45 años (veteranos)
- **Calificación/Potencial:** FIFA usa escala 0-99, pero valores <30 son errores de datos

### 4. Mapeo de columnas (inglés → español)

```python
mapeo_columnas = {
    'short_name': 'nombre',
    'age': 'edad',
    'overall': 'calificacion_general',
    'potential': 'potencial',
    'player_positions': 'posicion',
    'club_name': 'club',
    'nationality': 'nacionalidad',
    'value_eur': 'valor_mercado',
    'wage_eur': 'salario',
    'release_clause_eur': 'clausula_rescision'
}
```

**Propósito:** Estandarizar nombres de columnas en español para facilitar el trabajo.

---

## 🔧 Funciones del Pipeline (Detalladas)

### PASO 1: `leer_todas_hojas_con_anio()`

**Objetivo:** Cargar todas las hojas Excel y agregar columna `anio`.

#### ¿Cómo funciona?

```python
def leer_todas_hojas_con_anio(ruta_excel, mapa_hoja_anio=None):
    # 1. Cargar todas las hojas usando data_loader
    hojas = cargar_excel_completo(ruta_excel)
    
    # 2. Para cada hoja, inferir el año
    frames = []
    for nombre_hoja, df in hojas.items():
        # Inferir año desde nombre (ej: "fifa21" → 2021)
        anio = inferir_anio_desde_nombre_hoja(nombre_hoja)
        
        # Agregar columna 'anio'
        df['anio'] = anio
        frames.append(df)
    
    # 3. Concatenar todas las hojas en un solo DataFrame
    resultado = pd.concat(frames, ignore_index=True)
    return resultado
```

#### Ejemplo de inferencia de año:

| Nombre de hoja | Año inferido |
|----------------|--------------|
| `"fifa21"` | 2021 |
| `"FIFA 20"` | 2020 |
| `"fifa'19"` | 2019 |
| `"15"` | 2015 |

#### Salida:
```
DataFrame con 122,841 filas y 109 columnas (108 originales + 1 columna 'anio')
```

---

### PASO 2: `renombrar_columnas_dataset()`

**Objetivo:** Traducir nombres de columnas al español.

#### ¿Cómo funciona?

```python
def renombrar_columnas_dataset(df):
    # Crear diccionario solo con columnas que existen
    columnas_a_renombrar = {}
    for col_original, col_nueva in mapeo_columnas.items():
        if col_original in df.columns:
            columnas_a_renombrar[col_original] = col_nueva
    
    # Renombrar
    df_resultado = df.rename(columns=columnas_a_renombrar)
    return df_resultado
```

#### Transformación:

**ANTES:**
```
short_name | age | overall | potential | value_eur | ...
```

**DESPUÉS:**
```
nombre | edad | calificacion_general | potencial | valor_mercado | ...
```

---

### PASO 3: `eliminar_filas_resumen_y_fuera_rango()`

**Objetivo:** Eliminar filas de totales/resúmenes y valores fuera de rango.

#### ¿Cómo funciona?

```python
def eliminar_filas_resumen_y_fuera_rango(df, verbose=True):
    resultado = df.copy()
    stats = {
        'eliminadas_resumen': 0,
        'eliminadas_nulos_excesivos': 0,
        'eliminadas_edad_invalida': 0,
        'eliminadas_calificacion_invalida': 0,
        'eliminadas_potencial_invalido': 0,
        'ejemplos_edad_invalida': []
    }
    
    # 1. Eliminar filas de "resumen/totales" por heurística
    if "nombre" in resultado.columns:
        patron_resumen = r"\b(?:total|sum|average|promedio|summary)\b"
        mascara_resumen = resultado["nombre"].str.contains(
            patron_resumen, case=False, na=False, regex=True
        )
        stats['eliminadas_resumen'] = mascara_resumen.sum()
        resultado = resultado[~mascara_resumen]
    
    # 2. Eliminar filas con exceso de nulos
    ratio_nulos = resultado.isna().mean(axis=1)
    mascara_nulos = ratio_nulos > ratio_nulos_eliminar
    stats['eliminadas_nulos_excesivos'] = mascara_nulos.sum()
    resultado = resultado[~mascara_nulos]
    
    # 3. Validar rangos de edad, calificación, potencial
    def en_rango(col, minimo, maximo):
        return (resultado[col].between(minimo, maximo)) | (~resultado[col].notna())
    
    # Edad
    if "edad" in resultado.columns:
        mascara_edad = ~en_rango("edad", *rango_edad)
        stats['eliminadas_edad_invalida'] = mascara_edad.sum()
        
        # Capturar ejemplos
        if mascara_edad.sum() > 0:
            ejemplos = resultado[mascara_edad][['nombre','edad','anio']].head(3).to_dict('records')
            stats['ejemplos_edad_invalida'] = ejemplos
        
        resultado = resultado[en_rango("edad", *rango_edad)]
    
    # Similar para calificacion_general y potencial...
    
    return resultado, stats
```

#### Salida esperada:

```
📊 paso 3: limpieza de filas inválidas
  filas antes:   122,841
  filas después: 122,838
  🗑️ eliminadas:  3 filas (-0.00%)

  🔍 Ejemplos de jugadores eliminados por edad inválida:
      • Player X - edad: 50 años (año 2021)
      • Player Y - edad: 10 años (año 2019)
```

---

### PASO 4: `agregar_columnas_dinero_numericas()`

**Objetivo:** Asegurar que columnas monetarias sean `float`.

#### ¿Cómo funciona?

```python
def agregar_columnas_dinero_numericas(df):
    resultado = df.copy()
    columnas_dinero = ['valor_mercado', 'salario', 'clausula_rescision']
    
    for col in columnas_dinero:
        if col in resultado.columns:
            resultado[col] = resultado[col].apply(convertir_dinero_a_numero)
    
    return resultado

def convertir_dinero_a_numero(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan
```

#### Transformación:

| Valor original | Tipo original | Resultado | Tipo resultado |
|----------------|---------------|-----------|----------------|
| 1500000 | `int` | 1500000.0 | `float` |
| NaN | `float` | NaN | `float` |
| "1000" | `str` | 1000.0 | `float` |

---

### PASO 5: `eliminar_y_resolver_duplicados()`

**Objetivo:** Eliminar jugadores duplicados conservando el registro de mejor calidad.

#### Criterio de calidad:

1. **Menos valores nulos** → más completo es mejor
2. **Mayor calificación_general** → en caso de empate

#### ¿Cómo funciona?

```python
def eliminar_y_resolver_duplicados(df, verbose=True):
    resultado = df.copy()
    stats = {
        'duplicados_encontrados': 0,
        'duplicados_eliminados': 0,
        'ejemplos_duplicados': []
    }
    
    # 1. Contar duplicados por nombre+anio
    duplicados_antes = resultado.duplicated(subset=["nombre", "anio"], keep=False).sum()
    stats['duplicados_encontrados'] = duplicados_antes
    
    # 2. Capturar ejemplo ANTES de eliminar
    if duplicados_antes > 0:
        mascara_dup = resultado.duplicated(subset=["nombre", "anio"], keep=False)
        df_duplicados = resultado[mascara_dup].copy()
        primer_duplicado = df_duplicados.iloc[0]
        nombre_ej = primer_duplicado['nombre']
        anio_ej = primer_duplicado['anio']
        versiones = resultado[(resultado['nombre'] == nombre_ej) & (resultado['anio'] == anio_ej)]
        ejemplos = versiones[['nombre','anio','calificacion_general','club']].head(3).to_dict('records')
        stats['ejemplos_duplicados'] = ejemplos
    
    # 3. Calcular métrica de calidad
    conteo_no_nulos = resultado.notna().sum(axis=1)
    calificacion_general = resultado["calificacion_general"]
    resultado["_ranking_calidad"] = list(zip(conteo_no_nulos, calificacion_general))
    
    # 4. Ordenar y conservar el mejor
    resultado.sort_values(["nombre", "anio", "_ranking_calidad"], 
                         ascending=[True, True, False], inplace=True)
    resultado = resultado.drop_duplicates(subset=["nombre", "anio"], keep="first")
    resultado = resultado.drop(columns=["_ranking_calidad"])
    
    return resultado, stats
```

#### Salida esperada:

```
📊 paso 5: eliminación de duplicados
  filas antes:   122,838
  filas después: 116,079
  🗑️ eliminadas:  6,759 filas (-5.50%)

  🔍 Ejemplo de jugador duplicado (se conserva el de mayor calificación):
      ✅ CONSERVADO: L. Messi (2021) - Calif: 93 - Club: FC Barcelona
      🗑️ ELIMINADO: L. Messi (2021) - Calif: 92 - Club: PSG
```

---

### PASO 6: `imputar_y_llenar()`

**Objetivo:** Rellenar valores faltantes con estrategias inteligentes.

#### Estrategia por tipo de columna:

| Tipo | Columnas | Estrategia |
|------|----------|------------|
| **Categóricas** | club, nacionalidad, posicion | Rellenar con `"desconocido"` |
| **Numéricas** | edad, calificacion_general, potencial | Mediana por grupo (posicion+anio) |

#### ¿Cómo funciona?

```python
def imputar_y_llenar(df, verbose=True):
    resultado = df.copy()
    stats = {
        'nulos_antes': {},
        'nulos_despues': {},
        'valores_imputados': {},
        'ejemplos_imputacion_club': []
    }
    
    # 1. Categóricas a "desconocido"
    for col in ["club", "nacionalidad", "posicion"]:
        if col in resultado.columns:
            nulos = resultado[col].isna().sum()
            
            # Capturar ejemplos (solo para club)
            if col == "club" and nulos > 0:
                mascara_nulos = resultado[col].isna()
                ejemplos = resultado[mascara_nulos][['nombre','anio']].head(3).to_dict('records')
                stats['ejemplos_imputacion_club'] = ejemplos
            
            resultado[col] = resultado[col].fillna("desconocido")
            stats['valores_imputados'][col] = nulos
    
    # 2. Numéricas por mediana de grupo
    def imputar_por_grupo(col):
        # Estrategia en cascada:
        # 1. Mediana por posicion+anio
        resultado[col] = resultado.groupby(["posicion", "anio"])[col].transform(
            lambda s: s.fillna(s.median())
        )
        # 2. Fallback por anio
        resultado[col] = resultado.groupby(["anio"])[col].transform(
            lambda s: s.fillna(s.median())
        )
        # 3. Fallback global
        resultado[col] = resultado[col].fillna(resultado[col].median())
    
    for col in ["edad", "calificacion_general", "potencial"]:
        imputar_por_grupo(col)
    
    return resultado, stats
```

#### Ejemplo de imputación numérica:

**Escenario:** Portero de 2021 sin edad

1. **Paso 1:** Buscar mediana de porteros en 2021 → **32 años**
2. **Imputar:** Asignar 32 años
3. **Justificación:** Porteros tienden a ser mayores que delanteros

#### Salida esperada:

```
📊 paso 6: imputación de valores faltantes
  filas antes:   116,079
  filas después: 116,079
  📝 detalles: imputados -> club: 1,464 valores

  🔍 Ejemplos de jugadores sin club (se les asignó 'desconocido'):
      • J. Doe (2020) - club: [vacío] → 'desconocido'
      • A. Player (2019) - club: [vacío] → 'desconocido'
```

---

### PASO 7: `eliminar_filas_sin_objetivo()`

**Objetivo:** Eliminar jugadores sin `valor_mercado` (variable objetivo).

#### ¿Por qué?

En **regresión supervisada**, necesitamos el valor real (`y`) para entrenar el modelo. Sin `valor_mercado`, el registro es inútil.

#### ¿Cómo funciona?

```python
def eliminar_filas_sin_objetivo(df, verbose=True):
    resultado = df.copy()
    stats = {
        'filas_sin_valor_mercado': 0
    }
    
    if "valor_mercado" in resultado.columns:
        stats['filas_sin_valor_mercado'] = resultado["valor_mercado"].isna().sum()
        resultado = resultado[~resultado["valor_mercado"].isna()]
    
    return resultado, stats
```

#### Salida esperada:

```
📊 paso 7: eliminación de filas sin objetivo
  filas antes:   116,079
  filas después: 116,079
  🗑️ eliminadas:  0 filas (0.00%)

Resultado: ✅ Excelente! Todos los jugadores tienen valor de mercado.
```

---

### PASO 8: `seleccionar_columnas_para_ml()`

**Objetivo:** Reducir de 108 a 9 columnas esenciales para el modelo.

#### Columnas seleccionadas:

```python
columnas_ml = [
    "nombre",                # Identificación
    "anio",                  # Temporada
    "edad",                  # Factor clave
    "calificacion_general",  # Habilidad total
    "potencial",             # Potencial futuro
    "posicion",              # Rol en el campo
    "club",                  # Nivel del equipo
    "nacionalidad",          # Mercado
    "valor_mercado"          # Objetivo (target)
]
```

#### ¿Por qué eliminar 99 columnas?

**Razones:**

1. **Redundancia:** `calificacion_general` = promedio(pace, shooting, passing, defending, ...)
2. **Especificidad excesiva:** `curve`, `volleys` son muy específicos
3. **Correlación alta:** Estudios muestran que edad + calificación + potencial explican >80% de valor
4. **Principio de parsimonia:** Modelo simple primero, agregar features en etapa 3

#### ¿Cómo funciona?

```python
def seleccionar_columnas_para_ml(df, verbose=True):
    columnas_originales = list(df.columns)
    cols = ["nombre", "anio", "edad", "calificacion_general", "potencial", 
            "posicion", "club", "nacionalidad", "valor_mercado"]
    existentes = [c for c in cols if c in df.columns]
    resultado = df[existentes].copy()
    
    # Calcular columnas eliminadas
    cols_eliminadas = [c for c in columnas_originales if c not in existentes]
    
    stats = {
        'columnas_iniciales': len(columnas_originales),
        'columnas_finales': len(existentes),
        'columnas_eliminadas': len(cols_eliminadas),
        'lista_eliminadas': cols_eliminadas[:10]  # primeras 10
    }
    
    return resultado, stats
```

#### Salida esperada:

```
📊 paso 8: selección de columnas para ml
  columnas antes:   108
  columnas después: 9
  🗑️ eliminadas:    99 columnas

  🔍 Ejemplos de columnas eliminadas (primeras 10):
      pace, shooting, passing, dribbling, defending, physical,
      ball_control, curve, volleys, penalties
      ... y 89 más
```

---

## 🔄 Flujo Completo de Ejecución

### Diagrama de flujo:

```
[INICIO]
   ↓
[Paso 1] Cargar Excel → 122,841 filas × 108 cols
   ↓
[Paso 2] Renombrar columnas → inglés → español
   ↓
[Paso 3] Limpieza básica → 122,838 filas (-3)
   ↓
[Paso 4] Procesar dinero → conversión a float
   ↓
[Paso 5] Eliminar duplicados → 116,079 filas (-6,759)
   ↓
[Paso 6] Imputar valores → 1,464 clubes imputados
   ↓
[Paso 7] Filtrar sin objetivo → 116,079 filas (0 eliminadas)
   ↓
[Paso 8] Seleccionar columnas → 9 columnas (-99)
   ↓
[Paso 9] Reporte de calidad → estadísticas finales
   ↓
[Paso 10] Guardar CSV → jugadores_limpios.csv
   ↓
[FIN]
```

---

## 📊 Transformaciones Aplicadas

### Resumen de cambios:

| Etapa | Entrada | Salida | Cambio |
|-------|---------|--------|--------|
| **Inicio** | 122,841 × 108 | - | Dataset crudo |
| **Paso 3** | 122,841 | 122,838 | -3 filas (edad inválida) |
| **Paso 5** | 122,838 | 116,079 | -6,759 duplicados |
| **Paso 6** | 116,079 | 116,079 | +1,464 valores imputados |
| **Paso 7** | 116,079 | 116,079 | 0 sin valor_mercado |
| **Paso 8** | 116,079 × 108 | 116,079 × 9 | -99 columnas |
| **Final** | - | 116,079 × 9 | Dataset limpio |

### Tasa de retención:

```
Retención = (116,079 / 122,841) × 100 = 94.5%
```

✅ **Excelente:** Se conservó el 94.5% de los datos originales.

---

## 📝 Reportes y Ejemplos

### Sistema de reportes mejorado (v2.0):

Cada función del pipeline retorna:
```python
(DataFrame, Dict[estadisticas])
```

Las estadísticas incluyen:
- Conteos (filas eliminadas, valores imputados, etc.)
- **Ejemplos concretos** de registros afectados

#### Ejemplo de reporte visual:

```
======================================================================
📊 paso 5: eliminación de duplicados
======================================================================
  filas antes:   122,838
  filas después: 116,079
  🗑️ eliminadas:  6,759 filas (-5.50%)

  📝 detalles: encontrados: 11,730 registros duplicados, eliminados: 6,759

  🔍 Ejemplo de jugador duplicado (se conserva el de mayor calificación):
      ✅ CONSERVADO: L. Messi (2021) - Calif: 93 - Club: FC Barcelona
      🗑️ ELIMINADO: L. Messi (2021) - Calif: 92 - Club: PSG
      🗑️ ELIMINADO: L. Messi (2021) - Calif: 93 - Club: N/A
======================================================================
```

---

## 📤 Salidas y Resultados

### Archivo generado: `jugadores_limpios.csv`

**Estructura:**

```csv
nombre,anio,edad,calificacion_general,potencial,posicion,club,nacionalidad,valor_mercado
L. Messi,2021,34,93,93,RW,FC Barcelona,Argentina,78000000.0
Cristiano Ronaldo,2021,36,92,92,ST,Juventus,Portugal,45000000.0
Neymar Jr,2021,29,91,91,LW,Paris Saint-Germain,Brazil,100000000.0
...
```

**Estadísticas:**
- **Filas:** 116,079
- **Columnas:** 9
- **Tamaño:** ~15 MB
- **Completitud:** 100% (0% nulos)
- **Duplicados:** 0
- **Periodo:** 2015-2021

### Calidad del dataset final:

| Métrica | Valor |
|---------|-------|
| **Total registros** | 116,079 |
| **Valores nulos** | 0 (0%) |
| **Duplicados** | 0 |
| **Rango edad** | 14-45 años |
| **Rango calificación** | 30-99 |
| **Jugadores únicos** | ~18,000/año |

---

## ⚠️ Manejo de Errores

### Validaciones implementadas:

1. **Archivo Excel no encontrado**
   ```python
   if hojas is None:
       raise ValueError(f"no se pudo cargar el archivo excel: {ruta_excel}")
   ```

2. **Columnas faltantes**
   ```python
   if not {"nombre", "anio"}.issubset(resultado.columns):
       return resultado, stats  # Sin procesar
   ```

3. **Valores fuera de rango**
   ```python
   mascara_edad = ~en_rango("edad", 14, 45)
   resultado = resultado[~mascara_edad]  # Eliminar
   ```

---

## 🎯 Resumen Ejecutivo

### ¿Qué hace `pipeline.py`?
Convierte el dataset crudo de FIFA en un dataset limpio listo para Machine Learning.

### ¿Cómo lo hace?
Pipeline automatizado de 10 pasos con validaciones, imputaciones y selección de features.

### ¿Qué produce?
CSV con 116,079 jugadores, 9 columnas, 0% nulos, listo para regresión supervisada.

### Características clave:
- ✅ Automatizado (ejecuta con un comando)
- ✅ Robusto (maneja errores y casos especiales)
- ✅ Transparente (reportes con ejemplos concretos)
- ✅ Eficiente (94.5% de retención de datos)
- ✅ Documentado (estadísticas en cada paso)

---

**Fin de la documentación técnica**  
**Última actualización:** 19 de octubre de 2025
