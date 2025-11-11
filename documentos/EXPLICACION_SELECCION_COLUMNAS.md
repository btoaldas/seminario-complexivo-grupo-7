# 📋 SELECCIÓN DE COLUMNAS - EXPLICACIÓN DETALLADA

## ❓ ¿Por Qué Seleccionar Solo Algunas Columnas?

El dataset FIFA original tiene **106 columnas**, pero no todas son relevantes para nuestro análisis de scouting. Seleccionamos **61 columnas** (57%) por las siguientes razones:

### 🎯 Razones de la Selección

1. **Reducir ruido**: Muchas columnas tienen información redundante o irrelevante
2. **Mejorar rendimiento**: Menos columnas = procesamiento más rápido
3. **Facilitar análisis**: Enfocarse en atributos importantes para scouting
4. **Preparar para ML**: Seleccionar features predictivas del valor del jugador

---

## 📊 COLUMNAS SELECCIONADAS (61 total)

### 1️⃣ Información Básica del Jugador (14 columnas)

| Columna | Propósito |
|---------|-----------|
| `short_name` | Nombre corto para visualizaciones |
| `long_name` | Nombre completo para identificación única |
| `age` | Edad del jugador (importante para análisis) |
| `dob` | Fecha de nacimiento (calcular edad precisa) |
| `height_cm` | Altura en cm (físico del jugador) |
| `weight_kg` | Peso en kg (físico del jugador) |
| `nationality` | País de origen |
| `club_name` | Club actual |
| `league_name` | Liga donde juega |
| `player_positions` | Posiciones (ST, CM, GK, etc.) |
| `preferred_foot` | Pie dominante |
| `weak_foot` | Calidad del pie débil (1-5) |
| `skill_moves` | Habilidad de regates (1-5) |
| `work_rate` | Ritmo de trabajo (High/Medium/Low) |
| `body_type` | Tipo de cuerpo del jugador |

**Renombradas a español:**
- `nationality` → `nacionalidad`
- `long_name` → `nombre_completo`
- `age` → `edad`
- `player_positions` → `posiciones_jugador`

---

### 2️⃣ Valoración y Economía (5 columnas)

| Columna | Propósito | Variable Objetivo ML |
|---------|-----------|---------------------|
| `overall` | Valoración general FIFA (0-100) | ❌ Feature |
| `potential` | Potencial máximo (0-100) | ❌ Feature |
| `value_eur` | Valor de mercado en euros | ✅ **TARGET** |
| `wage_eur` | Salario semanal en euros | ❌ Feature |
| `release_clause_eur` | Cláusula de rescisión | ❌ Feature |

**¿Por qué `value_eur` es el objetivo?**
- Es la variable que queremos **predecir** en el modelo ML
- Representa el valor real de mercado del jugador
- Útil para detectar jugadores infravalorados

**Renombradas a español:**
- `overall` → `valoracion_global`
- `potential` → `potencial`
- `value_eur` → `valor_mercado_eur`
- `wage_eur` → `salario_eur`
- `release_clause_eur` → `clausula_rescision_eur`

---

### 3️⃣ Atributos Principales FIFA (6 columnas)

Las **6 categorías base** del sistema FIFA:

| Columna | Descripción | Rango |
|---------|-------------|-------|
| `pace` | Velocidad y aceleración | 0-100 |
| `shooting` | Calidad de tiro/disparo | 0-100 |
| `passing` | Precisión de pases | 0-100 |
| `dribbling` | Control del balón y regate | 0-100 |
| `defending` | Habilidades defensivas | 0-100 |
| `physic` | Fuerza física y resistencia | 0-100 |

**Renombradas a español:**
- `pace` → `ritmo_velocidad`
- `shooting` → `tiro_disparo`
- `passing` → `pase`
- `dribbling` → `regate_gambeta`
- `defending` → `defensa`
- `physic` → `fisico`

---

### 4️⃣ Atributos de Ataque (5 columnas)

| Columna | Descripción |
|---------|-------------|
| `attacking_crossing` | Calidad de centros |
| `attacking_finishing` | Definición/finalización |
| `attacking_heading_accuracy` | Precisión de cabezazos |
| `attacking_short_passing` | Pases cortos |
| `attacking_volleys` | Voleas |

**Renombradas a español:**
- `attacking_finishing` → `ataque_definicion`
- `attacking_crossing` → `ataque_centros`

---

### 5️⃣ Atributos de Habilidad/Técnica (5 columnas)

| Columna | Descripción |
|---------|-------------|
| `skill_dribbling` | Regate individual |
| `skill_curve` | Efecto en el balón |
| `skill_fk_accuracy` | Precisión en tiros libres |
| `skill_long_passing` | Pases largos |
| `skill_ball_control` | Control del balón |

**Renombradas a español:**
- `skill_dribbling` → `habilidad_regate`
- `skill_curve` → `habilidad_efecto`

---

### 6️⃣ Atributos de Movimiento (5 columnas)

| Columna | Descripción |
|---------|-------------|
| `movement_acceleration` | Aceleración |
| `movement_sprint_speed` | Velocidad máxima |
| `movement_agility` | Agilidad |
| `movement_reactions` | Tiempo de reacción |
| `movement_balance` | Equilibrio |

**Renombradas a español:**
- `movement_acceleration` → `movimiento_aceleracion`
- `movement_sprint_speed` → `movimiento_velocidad_sprint`

---

### 7️⃣ Atributos de Potencia (5 columnas)

| Columna | Descripción |
|---------|-------------|
| `power_shot_power` | Potencia de disparo |
| `power_jumping` | Salto |
| `power_stamina` | Resistencia |
| `power_strength` | Fuerza física |
| `power_long_shots` | Tiros de larga distancia |

**Renombradas a español:**
- `power_shot_power` → `potencia_disparo`
- `power_stamina` → `potencia_resistencia`

---

### 8️⃣ Atributos Mentales (6 columnas)

| Columna | Descripción |
|---------|-------------|
| `mentality_aggression` | Agresividad |
| `mentality_interceptions` | Intercepciones |
| `mentality_positioning` | Posicionamiento |
| `mentality_vision` | Visión de juego |
| `mentality_penalties` | Penales |
| `mentality_composure` | Compostura bajo presión |

**Renombradas a español:**
- `mentality_aggression` → `mentalidad_agresividad`
- `mentality_vision` → `mentalidad_vision`

---

### 9️⃣ Atributos de Defensa (3 columnas)

| Columna | Descripción |
|---------|-------------|
| `defending_marking` | Marcaje | ✅ **Corregido**
| `defending_standing_tackle` | Entrada de pie |
| `defending_sliding_tackle` | Entrada deslizante |

**⚠️ Corrección realizada:**
- ❌ ANTES: Buscábamos `defending_marking_awareness` (no existe)
- ✅ AHORA: Usamos `defending_marking` (nombre real)

**Renombradas a español:**
- `defending_marking` → `defensa_marcaje`
- `defending_standing_tackle` → `defensa_entrada_pie`

---

### 🔟 Atributos de Portero (5 columnas)

| Columna | Descripción |
|---------|-------------|
| `goalkeeping_diving` | Estiradas |
| `goalkeeping_handling` | Manejo del balón |
| `goalkeeping_kicking` | Saque de meta |
| `goalkeeping_positioning` | Colocación |
| `goalkeeping_reflexes` | Reflejos |

**Renombradas a español:**
- `goalkeeping_diving` → `gk_portero_estirada`
- `goalkeeping_handling` → `gk_portero_manejo`
- `goalkeeping_reflexes` → `gk_portero_reflejos`

---

### 1️⃣1️⃣ Metadatos (1 columna adicional)

| Columna | Descripción |
|---------|-------------|
| `año_datos` | Año del dataset (2015-2021) |

Esta columna se **agrega automáticamente** durante la carga para trackear de qué edición FIFA viene cada jugador.

---

## ❌ COLUMNAS EXCLUIDAS (45 columnas)

### ¿Qué columnas NO seleccionamos y por qué?

#### 1. **Columnas de Identificación Técnica**
- `sofifa_id`: ID interno de SoFIFA (no aporta al análisis)
- `player_url`: URL del perfil (no útil para ML)
- `player_face_url`: URL de la foto (no útil)
- `club_logo_url`: URL del logo del club

**Razón:** Son metadatos técnicos sin valor predictivo.

#### 2. **Columnas de Contexto No Esencial**
- `club_position`: Posición en el club específico
- `club_jersey_number`: Número de camiseta
- `club_loaned_from`: Club de origen si está cedido
- `club_joined`: Fecha de unión al club
- `contract_valid_until`: Vigencia del contrato
- `nation_position`: Posición en selección
- `nation_jersey_number`: Número en selección

**Razón:** Información contextual que cambia frecuentemente y no afecta el valor intrínseco del jugador.

#### 3. **Columnas de Reputación y Rankings**
- `international_reputation`: Reputación (1-5)
- `league_rank`: Ranking de la liga

**Razón:** Correlacionan altamente con `overall` (redundantes).

#### 4. **Atributos Muy Específicos de Posición**
- `ls`, `st`, `rs`, `lw`, `lf`, `cf`, `rf`, `rw`, `lam`, `cam`, `ram`, `lm`, `lcm`, `cm`, `rcm`, `rm`, `lwb`, `ldm`, `cdm`, `rdm`, `rwb`, `lb`, `lcb`, `cb`, `rcb`, `rb`

**Razón:** Son ratings calculados para cada posición específica (28 columnas). Mantenemos `player_positions` que es más general.

#### 5. **Columnas Calculadas/Derivadas**
- `player_traits`: Rasgos especiales (texto)
- `player_tags`: Etiquetas (texto)

**Razón:** Son combinaciones de otros atributos. Podemos crear features similares en Feature Engineering.

---

## ✅ CORRECCIONES REALIZADAS

### Problema Original
```
• Columnas totales originales: 107
• Columnas relevantes encontradas: 59
• Columnas no encontradas: 2
   • nationality_name  ❌ No existe
   • defending_marking_awareness  ❌ No existe
```

### Solución Aplicada

| Columna Buscada (Incorrecta) | Columna Real | Estado |
|------------------------------|--------------|--------|
| `nationality_name` ❌ | `nationality` ✅ | Corregido |
| `defending_marking_awareness` ❌ | `defending_marking` ✅ | Corregido |

**Resultado después de corrección:**
```
• Columnas totales originales: 107
• Columnas relevantes encontradas: 61  ✅ (+2)
• Columnas no encontradas: 0  ✅
```

---

## 📈 JUSTIFICACIÓN POR CASOS DE USO

### Para Scouting de Jugadores
✅ **Necesitamos:**
- Atributos físicos y técnicos completos
- Valoración y potencial
- Información de club y posición
- Económico (valor, salario)

❌ **NO necesitamos:**
- URLs de imágenes
- IDs internos
- Números de camiseta
- Fechas de contrato

### Para Machine Learning (Predecir Valor)
✅ **Features importantes:**
- Atributos de juego (60+ columnas)
- Edad y físico
- Overall y potential
- Posición

❌ **Features no útiles:**
- Metadatos técnicos
- Información contractual
- Reputación (correlaciona con overall)

### Para Análisis de Dashboard
✅ **Para visualizar:**
- Nombres y clubs
- Atributos comparables
- Estadísticas agregadas
- Filtros por posición/liga

❌ **Difícil de visualizar:**
- URLs
- IDs
- Atributos de texto largo

---

## 🎯 RESUMEN

| Concepto | Valor |
|----------|-------|
| **Columnas originales** | 106 |
| **Columnas seleccionadas** | 61 (57%) |
| **Columnas excluidas** | 45 (43%) |
| **Errores corregidos** | 2 columnas |

**Principio aplicado:**
> "Seleccionar solo lo necesario, pero todo lo importante"

**Resultado:**
- ✅ Dataset más limpio y rápido
- ✅ Sin columnas faltantes
- ✅ Todas las columnas relevantes incluidas
- ✅ Listas para renombrar a español

---

**Fecha:** 8 de noviembre de 2025  
**Archivo:** `backend/scripts/limpieza_datos.py`  
**Función:** `seleccionar_columnas_relevantes()`
