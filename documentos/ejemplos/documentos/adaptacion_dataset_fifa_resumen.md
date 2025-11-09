# RESUMEN: ADAPTACIÓN DEL CÓDIGO AL DATASET FIFA

**Fecha:** Enero 2025  
**Dataset:** FIFA 15-21 (7 hojas, 106 columnas, ~122,800 registros)  
**Objetivo:** Adaptar funciones de limpieza de un dataset de videojuegos al dataset real de jugadores de FIFA

---

## 1. CONTEXTO DEL PROYECTO

### Dataset Original
- **Fuente:** Videojuegos (games.csv)
- **Columnas clave:** Name, Genre, Year_of_Release, User_Score, Rating_ESRB

### Dataset FIFA
- **Fuente:** FIFA 15-21 (dataset.xlsx)
- **Estructura:** 7 hojas (una por año), 106 columnas por hoja
- **Registros:** ~18,000 jugadores por año, total 122,838 registros
- **Columnas clave:** 
  - Identificación: sofifa_id, short_name, long_name, age, nationality
  - Carrera: club_name, league_name, value_eur, wage_eur, player_positions
  - Habilidades: overall, potential, pace, shooting, passing, dribbling, defending, physic
  - Posiciones: 30+ columnas de rating por posición (ST, LW, CAM, etc.)
  - Porteros: gk_diving, gk_handling, gk_kicking, gk_reflexes, etc.

---

## 2. FUNCIONES ADAPTADAS

### 2.1. limpieza_nombres_columnas()
**Cambios:**
- Columnas renombradas de inglés a español
- Mapeo específico para FIFA:
  - `short_name` → `nombre`
  - `player_positions` → `posicion`
  - `club_name` → `club`
  - `league_name` → `liga`
  - `value_eur` → `valor_mercado`
  - `wage_eur` → `salario`

**Ejemplo:**
```python
# Antes (videojuegos)
"Name": "videogame_names"

# Después (FIFA)
"short_name": "nombre",
"player_positions": "posicion"
```

### 2.2. convertir_edad_int() [antes: convertir_anio_int()]
**Cambios:**
- Función renombrada para reflejar su nuevo propósito
- Columna cambiada de `year_of_release` a `age`
- Mantiene conversión a Int64 con manejo de NaN

**Justificación:**
- Dataset FIFA ya tiene columna `age` (edad del jugador)
- No tiene columna `year_of_release` (año se obtiene del nombre de la hoja)

### 2.3. limpieza_valores_monetarios() [antes: limpieza_user_score_tbd()]
**Cambios:**
- Reemplazo completo de la lógica
- **Antes:** Limpiaba columna `user_score` reemplazando 'tbd' con NaN
- **Después:** Limpia columnas `valor_mercado` y `salario` con pd.to_numeric()

**Código adaptado:**
```python
def limpieza_valores_monetarios(df):
    """
    limpia las columnas valor_mercado y salario
    convirtiendo a numérico y manejando errores
    """
    df["valor_mercado"] = pd.to_numeric(df["valor_mercado"], errors='coerce')
    df["salario"] = pd.to_numeric(df["salario"], errors='coerce')
    return df
```

### 2.4. eliminar_filas_info_faltantes()
**Cambios:**
- Adaptación de columnas críticas para filtrado
- **Primera fase:** 
  - Antes: ["videogame_names", "genre"]
  - Después: ["nombre", "posicion"]
- **Segunda fase:**
  - Antes: ["year_of_release", "critic_score", "user_score", "rating_esrb"]
  - Después: ["overall", "potential", "valor_mercado", "club"]

**Lógica:** Mantiene el filtrado en dos niveles (crítico y secundario)

### 2.5. rellenar_valores_club() [antes: rellenar_valores_esrb()]
**Cambios:**
- Función renombrada y adaptada
- **Antes:** Rellenaba `rating_esrb` con "RP" (Rating Pending)
- **Después:** Rellena `club` con "Sin Club" (Free Agent)

**Justificación:**
- Jugadores sin club son agentes libres o retirados
- Total de 1,569 jugadores sin club en el dataset

---

## 3. FUNCIONES NUEVAS AGREGADAS

### 3.1. agregar_columna_anio(df, anio)
**Propósito:** Agregar columna de año para identificar versión de FIFA

**Ejemplo:**
```python
# FIFA 15 → anio = 2015
# FIFA 16 → anio = 2016
df = agregar_columna_anio(df, 2015)
```

### 3.2. eliminar_duplicados(df)
**Propósito:** Eliminar jugadores duplicados por `sofifa_id`

**Resultado:** 0 duplicados encontrados en cada hoja individual

### 3.3. validar_rangos_numericos(df)
**Propósito:** Validar que los datos estén en rangos lógicos

**Criterios:**
- Edad: 15-45 años
- Overall y Potential: 0-100
- Valores monetarios: no negativos

**Resultado:** 
- FIFA 15: 16,155 → 16,155 (0 eliminados)
- FIFA 17: 17,597 → 17,596 (1 eliminado)
- FIFA 18: 17,954 → 17,953 (1 eliminado)
- FIFA 21: 18,944 → 18,943 (1 eliminado)

---

## 4. PIPELINE COMPLETO IMPLEMENTADO

### Archivo: main_fifa.py

**Estructura:**
1. Cargar las 7 hojas del Excel (FIFA 15-21)
2. Para cada hoja:
   - Limpieza de nombres de columnas
   - Conversión de edad a Int64
   - Limpieza de valores monetarios
   - Eliminación de filas con info faltante
   - Rellenar valores NaN en club
   - Agregar columna año
   - Eliminar duplicados
   - Validar rangos numéricos
3. Concatenar todos los dataframes
4. Eliminar duplicados globales (sofifa_id + anio)
5. Guardar CSV final

**Archivo de salida:** `data/jugadores_fifa_limpio.csv`

---

## 5. RESULTADOS DEL PIPELINE

### Dimensiones Finales
- **Total de registros:** 122,838 jugadores
- **Total de columnas:** 107 (106 originales + 1 columna 'anio')

### Distribución por Año
| Año  | Jugadores |
|------|-----------|
| 2015 | 16,155    |
| 2016 | 15,623    |
| 2017 | 17,596    |
| 2018 | 17,953    |
| 2019 | 18,085    |
| 2020 | 18,483    |
| 2021 | 18,943    |

### Estadísticas Generales
- **Edad promedio:** 25.1 años
- **Overall promedio:** 65.7
- **Valor de mercado promedio:** €2,045,563
- **Salario promedio:** €11,235

### Top 5 Clubes con Más Jugadores
1. Sin Club: 1,569 jugadores (agentes libres)
2. Arsenal: 230 jugadores
3. West Ham United: 229 jugadores
4. Leicester City: 229 jugadores
5. Southampton: 229 jugadores

---

## 6. VALIDACIÓN Y PRUEBAS

### Script de Prueba: prueba_limpieza_fifa.py
- Prueba cada función individualmente con FIFA 21
- Valida tipos de datos, dimensiones y resultados
- Resultado: ✓ Todas las funciones probadas exitosamente

### Ejecución del Pipeline Completo
- Comando: `python main_fifa.py`
- Resultado: ✓ Pipeline completado exitosamente
- Archivo generado: `data/jugadores_fifa_limpio.csv`

---

## 7. MAPEO DE COLUMNAS

### Columnas Clave Utilizadas

| Columna Original FIFA | Columna Renombrada | Tipo      | Descripción                    |
|-----------------------|--------------------|-----------|--------------------------------|
| sofifa_id             | sofifa_id          | int64     | ID único del jugador           |
| short_name            | nombre             | object    | Nombre corto                   |
| player_positions      | posicion           | object    | Posiciones del jugador         |
| club_name             | club               | object    | Nombre del club                |
| league_name           | liga               | object    | Nombre de la liga              |
| age                   | age                | Int64     | Edad del jugador               |
| overall               | overall            | int64     | Calificación general           |
| potential             | potential          | int64     | Potencial del jugador          |
| value_eur             | valor_mercado      | int64     | Valor de mercado (euros)       |
| wage_eur              | salario            | int64     | Salario semanal (euros)        |
| (nombre de hoja)      | anio               | int64     | Año de la versión FIFA         |

### Columnas Adicionales Disponibles (no renombradas)
- Físicas: height_cm, weight_kg, body_type, preferred_foot
- Habilidades: pace, shooting, passing, dribbling, defending, physic
- Posiciones específicas: ST, LW, RW, CAM, CM, CDM, CB, LB, RB, GK (30+ columnas)
- Porteros: gk_diving, gk_handling, gk_kicking, gk_reflexes, gk_speed, gk_positioning
- Contratos: release_clause_eur, contract_valid_until
- Enlaces: player_url, player_face_url

---

## 8. MEJORAS IMPLEMENTADAS

### Respecto al Código Original
1. **Nombres descriptivos:** Funciones renombradas para reflejar su propósito real
2. **Validaciones agregadas:** Función `validar_rangos_numericos()` para datos lógicos
3. **Manejo de años:** Sistema automático para agregar columna año por hoja
4. **Pipeline completo:** Procesamiento de las 7 hojas con concatenación final
5. **Estadísticas detalladas:** Reportes por fase y resumen final
6. **Eliminación de duplicados:** A nivel individual y global

### Archivos Generados
- ✓ `scripts_fifa/data_cleaning.py` - 8 funciones adaptadas
- ✓ `main_fifa.py` - Pipeline orquestador completo
- ✓ `prueba_limpieza_fifa.py` - Script de validación
- ✓ `data/jugadores_fifa_limpio.csv` - Dataset final limpio

---

## 9. PRÓXIMOS PASOS SUGERIDOS

### Análisis Exploratorio (EDA)
1. Distribución de edades por posición
2. Correlación entre overall, potential y valor_mercado
3. Evolución de valores a través de los años (2015-2021)
4. Top jugadores por overall y valor de mercado
5. Análisis de clubes y ligas más valiosos

### Feature Engineering
1. Crear categorías de edad (joven, maduro, veterano)
2. Clasificar posiciones (delantero, mediocampista, defensa, portero)
3. Calcular diferencia entre potential y overall (margen de crecimiento)
4. Normalizar valores monetarios por año
5. Crear índice de valor por edad

### Machine Learning
1. Modelo de regresión para predecir valor_mercado
2. Variables predictoras: age, overall, potential, posicion, liga, anio
3. Detección de jugadores infravalorados (valor real < valor predicho)
4. Validación del modelo con métricas (MAE, R², RMSE)

### Dashboard y Visualización
1. Dashboard interactivo con Streamlit
2. Filtros por año, posición, club, liga
3. Gráficos de distribución y correlación
4. Sistema de búsqueda de jugadores
5. Comparación de jugadores

---

## 10. CONCLUSIONES

### Logros
✓ **Adaptación completa** de 5 funciones del código original  
✓ **3 funciones nuevas** específicas para dataset FIFA  
✓ **Pipeline funcional** procesando 122,838 registros  
✓ **Validación exitosa** de todas las funciones  
✓ **Dataset limpio** generado y listo para análisis  

### Calidad de Datos
- **Datos consistentes:** Rangos numéricos validados
- **Sin duplicados:** Sistema de detección implementado
- **Valores completos:** NaN manejados apropiadamente
- **Estructura uniforme:** 107 columnas en todas las filas

### Cumplimiento de Estándares (AGENTS.md)
✓ snake_case en todo el código  
✓ Sin tildes en nombres de variables  
✓ Comentarios en español con tildes  
✓ Documentación completa en funciones  
✓ Código limpio y mantenible  

---

**Elaborado por:** Copilot GitHub  
**Proyecto:** Sistema de Scouting FIFA - Seminario Complexivo Grupo 7  
**Dataset:** FIFA 15-21 (122,838 jugadores)
