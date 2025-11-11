# 🎨 GUÍA PARA USAR COLUMNAS DE URL Y FOTOS EN EL DASHBOARD

## 📋 COLUMNAS AÑADIDAS PARA EL DASHBOARD

Hemos incluido **3 columnas adicionales** específicamente para mejorar el dashboard:

| Columna Original | Nombre en Español | Propósito Dashboard |
|-----------------|-------------------|---------------------|
| `sofifa_id` | `id_sofifa` | Identificador único para referencias |
| `player_url` | `url_jugador` | URL de SoFIFA con info completa + foto |
| `real_face` | `tiene_foto_real` | Indica si tiene foto real (True/False) |

---

## 🖼️ CÓMO OBTENER LA FOTO DEL JUGADOR

### Estructura de URL de SoFIFA

La columna `url_jugador` contiene URLs como:
```
https://sofifa.com/player/158023/lionel-messi/210021
```

### Patrón para Extraer Foto

SoFIFA usa este formato para las fotos de jugadores:

```python
# URL del jugador
url_jugador = "https://sofifa.com/player/158023/lionel-messi/210021"

# Extraer el ID del jugador (primer número después de /player/)
import re
player_id = re.search(r'/player/(\d+)/', url_jugador).group(1)
# Resultado: "158023"

# Construir URL de la foto
foto_url = f"https://cdn.sofifa.net/players/{player_id[:3]}/{player_id[:3]}/{player_id}.png"
# Resultado: "https://cdn.sofifa.net/players/158/023/158023.png"
```

### Implementación en Streamlit

```python
import streamlit as st
import pandas as pd
import re

def obtener_url_foto(url_jugador):
    """
    Extrae el ID del jugador y construye la URL de la foto.
    
    Args:
        url_jugador: URL de SoFIFA (ej: "https://sofifa.com/player/158023/...")
        
    Returns:
        URL de la foto del jugador
    """
    if pd.isna(url_jugador):
        return None
    
    # Extraer ID del jugador
    match = re.search(r'/player/(\d+)/', str(url_jugador))
    if not match:
        return None
    
    player_id = match.group(1)
    
    # Construir URL de foto
    # Formato: cdn.sofifa.net/players/XXX/XXX/XXXXXX.png
    # Donde XXX son los primeros 3 dígitos del ID
    foto_url = f"https://cdn.sofifa.net/players/{player_id[:3]}/{player_id[:3]}/{player_id}.png"
    
    return foto_url


# Ejemplo de uso en el dashboard
st.title("Perfil del Jugador")

# Cargar datos
df = pd.read_csv('datos/fifa_limpio.csv')
jugador = df[df['nombre_completo'] == 'Lionel Messi'].iloc[0]

# Obtener foto
foto_url = obtener_url_foto(jugador['url_jugador'])

# Mostrar foto
if foto_url:
    st.image(foto_url, width=150, caption=jugador['nombre_completo'])
else:
    st.info("Foto no disponible")

# Botón para ver más info
if st.button("Ver más información"):
    st.markdown(f"[Perfil completo en SoFIFA]({jugador['url_jugador']})")
```

---

## 🕷️ CÓMO CREAR GRÁFICOS RADAR (ARAÑA)

### Datos Necesarios

Para un gráfico radar del jugador, usamos los **6 atributos principales**:

```python
atributos_radar = [
    'ritmo_velocidad',
    'tiro_disparo', 
    'pase',
    'regate_gambeta',
    'defensa',
    'fisico'
]
```

### Implementación con Plotly

```python
import plotly.graph_objects as go

def crear_grafico_radar(jugador_data, nombre_jugador):
    """
    Crea un gráfico radar con los 6 atributos principales del jugador.
    
    Args:
        jugador_data: Serie de pandas con los datos del jugador
        nombre_jugador: Nombre del jugador para el título
        
    Returns:
        Figura de Plotly
    """
    # Atributos para el radar
    categorias = [
        'Ritmo/Velocidad',
        'Tiro/Disparo',
        'Pase',
        'Regate',
        'Defensa',
        'Físico'
    ]
    
    # Valores del jugador (ya en español)
    valores = [
        jugador_data['ritmo_velocidad'],
        jugador_data['tiro_disparo'],
        jugador_data['pase'],
        jugador_data['regate_gambeta'],
        jugador_data['defensa'],
        jugador_data['fisico']
    ]
    
    # Crear gráfico radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name=nombre_jugador,
        line=dict(color='#00D9FF', width=2),
        fillcolor='rgba(0, 217, 255, 0.3)'
    ))
    
    # Configurar layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=True,
        title=f"Atributos de {nombre_jugador}",
        height=500
    )
    
    return fig


# Ejemplo de uso en Streamlit
st.subheader("📊 Análisis de Atributos")

# Seleccionar jugador
jugador_seleccionado = st.selectbox(
    "Selecciona un jugador",
    df['nombre_completo'].unique()
)

# Obtener datos del jugador
jugador = df[df['nombre_completo'] == jugador_seleccionado].iloc[0]

# Crear y mostrar gráfico radar
col1, col2 = st.columns([1, 2])

with col1:
    # Mostrar foto
    foto_url = obtener_url_foto(jugador['url_jugador'])
    if foto_url:
        st.image(foto_url, width=150)
    
    # Estadísticas básicas
    st.metric("Overall", jugador['valoracion_global'])
    st.metric("Potencial", jugador['potencial'])
    st.metric("Valor", f"€{jugador['valor_mercado_eur']:,.0f}")

with col2:
    # Gráfico radar
    fig = crear_grafico_radar(jugador, jugador['nombre_completo'])
    st.plotly_chart(fig, use_container_width=True)
```

---

## 🔄 COMPARACIÓN DE JUGADORES (RADAR DUAL)

### Comparar 2 Jugadores

```python
def crear_radar_comparativo(jugador1_data, jugador2_data, nombre1, nombre2):
    """
    Crea un gráfico radar comparando 2 jugadores.
    """
    categorias = [
        'Ritmo/Velocidad',
        'Tiro/Disparo',
        'Pase',
        'Regate',
        'Defensa',
        'Físico'
    ]
    
    # Valores jugador 1
    valores1 = [
        jugador1_data['ritmo_velocidad'],
        jugador1_data['tiro_disparo'],
        jugador1_data['pase'],
        jugador1_data['regate_gambeta'],
        jugador1_data['defensa'],
        jugador1_data['fisico']
    ]
    
    # Valores jugador 2
    valores2 = [
        jugador2_data['ritmo_velocidad'],
        jugador2_data['tiro_disparo'],
        jugador2_data['pase'],
        jugador2_data['regate_gambeta'],
        jugador2_data['defensa'],
        jugador2_data['fisico']
    ]
    
    fig = go.Figure()
    
    # Jugador 1
    fig.add_trace(go.Scatterpolar(
        r=valores1,
        theta=categorias,
        fill='toself',
        name=nombre1,
        line=dict(color='#00D9FF', width=2),
        fillcolor='rgba(0, 217, 255, 0.3)'
    ))
    
    # Jugador 2
    fig.add_trace(go.Scatterpolar(
        r=valores2,
        theta=categorias,
        fill='toself',
        name=nombre2,
        line=dict(color='#FF6B6B', width=2),
        fillcolor='rgba(255, 107, 107, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title=f"Comparación: {nombre1} vs {nombre2}",
        height=600
    )
    
    return fig


# Uso en dashboard
st.subheader("⚔️ Comparación de Jugadores")

col1, col2 = st.columns(2)

with col1:
    jugador1 = st.selectbox("Jugador 1", df['nombre_completo'].unique(), key='j1')

with col2:
    jugador2 = st.selectbox("Jugador 2", df['nombre_completo'].unique(), key='j2')

if st.button("Comparar"):
    j1_data = df[df['nombre_completo'] == jugador1].iloc[0]
    j2_data = df[df['nombre_completo'] == jugador2].iloc[0]
    
    # Fotos
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        foto1 = obtener_url_foto(j1_data['url_jugador'])
        if foto1:
            st.image(foto1, width=120)
        st.metric("Overall", j1_data['valoracion_global'])
    
    with col2:
        fig = crear_radar_comparativo(j1_data, j2_data, jugador1, jugador2)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        foto2 = obtener_url_foto(j2_data['url_jugador'])
        if foto2:
            st.image(foto2, width=120)
        st.metric("Overall", j2_data['valoracion_global'])
```

---

## 📊 GRÁFICO RADAR AVANZADO (TODOS LOS ATRIBUTOS)

### Radar Detallado con Subatributos

```python
def crear_radar_detallado(jugador_data, nombre_jugador):
    """
    Crea un radar con más detalles: ataque, defensa, físico, mental.
    """
    # Categorías expandidas
    categorias = [
        'Aceleración',
        'Velocidad Sprint',
        'Finalización',
        'Disparo Potencia',
        'Pase Corto',
        'Pase Largo',
        'Regate',
        'Control Balón',
        'Marcaje',
        'Entrada',
        'Resistencia',
        'Fuerza',
        'Agresividad',
        'Visión'
    ]
    
    valores = [
        jugador_data['movimiento_aceleracion'],
        jugador_data['movimiento_velocidad_sprint'],
        jugador_data['ataque_definicion'],
        jugador_data['potencia_disparo'],
        jugador_data['ataque_pase_corto'],
        jugador_data['habilidad_pase_largo'],
        jugador_data['habilidad_regate'],
        jugador_data['habilidad_control_balon'],
        jugador_data['defensa_marcaje'],
        jugador_data['defensa_entrada_pie'],
        jugador_data['potencia_resistencia'],
        jugador_data['potencia_fuerza'],
        jugador_data['mentalidad_agresividad'],
        jugador_data['mentalidad_vision']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name=nombre_jugador,
        line=dict(color='#4ECDC4', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title=f"Análisis Detallado: {nombre_jugador}",
        height=700
    )
    
    return fig
```

---

## 🎯 EJEMPLO COMPLETO DE TAB EN DASHBOARD

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('datos/fifa_limpio.csv')

df = cargar_datos()


# TAB: PERFIL DE JUGADOR
def tab_perfil_jugador():
    st.title("👤 Perfil de Jugador")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar jugador por nombre")
    
    if busqueda:
        resultados = df[df['nombre_completo'].str.contains(busqueda, case=False, na=False)]
        
        if len(resultados) > 0:
            jugador_seleccionado = st.selectbox(
                "Selecciona un jugador",
                resultados['nombre_completo'].tolist()
            )
            
            jugador = df[df['nombre_completo'] == jugador_seleccionado].iloc[0]
            
            # Layout con 3 columnas
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.subheader("📸 Foto")
                foto_url = obtener_url_foto(jugador['url_jugador'])
                if foto_url:
                    st.image(foto_url, width=150)
                else:
                    st.info("Sin foto")
                
                # Link a SoFIFA
                if not pd.isna(jugador['url_jugador']):
                    st.markdown(f"[📊 Ver en SoFIFA]({jugador['url_jugador']})")
            
            with col2:
                st.subheader("📊 Atributos Principales")
                fig = crear_grafico_radar(jugador, jugador_seleccionado)
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.subheader("📈 Estadísticas")
                st.metric("Overall", jugador['valoracion_global'])
                st.metric("Potencial", jugador['potencial'])
                st.metric("Edad", jugador['edad'])
                st.metric("Valor", f"€{jugador['valor_mercado_eur']:,.0f}")
                st.metric("Salario", f"€{jugador['salario_eur']:,.0f}")
            
            # Información adicional
            st.subheader("ℹ️ Información")
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.write(f"**Club:** {jugador['club']}")
                st.write(f"**Liga:** {jugador['liga']}")
            
            with col_info2:
                st.write(f"**Posición:** {jugador['posiciones_jugador']}")
                st.write(f"**Nacionalidad:** {jugador['nacionalidad']}")
            
            with col_info3:
                st.write(f"**Altura:** {jugador['altura_cm']} cm")
                st.write(f"**Peso:** {jugador['peso_kg']} kg")


# Ejecutar
if __name__ == "__main__":
    tab_perfil_jugador()
```

---

## ✅ RESUMEN DE CAMBIOS REALIZADOS

### Columnas Añadidas

| Columna Original | Español | Uso Dashboard |
|-----------------|---------|---------------|
| `sofifa_id` | `id_sofifa` | Identificador único |
| `player_url` | `url_jugador` | Link a SoFIFA + construir URL foto |
| `real_face` | `tiene_foto_real` | Filtrar jugadores con foto |

### Total de Columnas Ahora

```
ANTES: 61 columnas
DESPUÉS: 64 columnas (+3)
```

### Beneficios

✅ **Fotos de jugadores** en el dashboard  
✅ **Links** a información completa en SoFIFA  
✅ **Gráficos radar** con datos completos  
✅ **Comparaciones visuales** entre jugadores  
✅ **Mejor experiencia** de usuario en el dashboard  

---

**Archivos actualizados:**
- ✅ `backend/scripts/limpieza_datos.py` → Añadidas 3 columnas
- ✅ `backend/scripts/renombrado_columnas.py` → Mapeo a español

**Próximos pasos:**
1. Ejecutar pipeline: `python backend/pipeline_limpieza_datos.py`
2. Implementar funciones en `frontend/dashboard_scouting.py`
3. Crear tab de perfil de jugador con foto y radar

---

**Fecha:** 8 de noviembre de 2025  
**Estado:** ✅ Columnas agregadas y listas para usar
