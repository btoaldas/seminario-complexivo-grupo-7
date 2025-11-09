import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="⚽ FIFA Scouting Pro | Dashboard ML",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES MODERNA
COLOR_PRIMARIO = "#0A1929"  # Azul oscuro elegante
COLOR_SECUNDARIO = "#1E88E5"  # Azul brillante
COLOR_ACENTO_1 = "#00ACC1"  # Cyan
COLOR_ACENTO_2 = "#132F4C"  # Azul medio oscuro
COLOR_DESTACADO = "#FFA726"  # Naranja dorado
COLOR_EXITO = "#66BB6A"  # Verde
COLOR_PELIGRO = "#EF5350"  # Rojo
COLOR_ADVERTENCIA = "#FDD835"  # Amarillo

# CSS PERSONALIZADO MEJORADO
st.markdown(f"""
<style>
    /* Fondo principal */
    .stApp {{
        background: linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO_2} 100%);
    }}
    
    /* Métricas mejoradas */
    .stMetric {{
        background: linear-gradient(145deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid {COLOR_DESTACADO};
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }}
    .stMetric:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }}
    .stMetric label {{
        color: {COLOR_SECUNDARIO} !important;
        font-weight: 600;
        font-size: 14px;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: white !important;
        font-size: 32px;
        font-weight: bold;
    }}
    
    /* Ficha de jugador mejorada */
    .ficha-jugador {{
        background: linear-gradient(145deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%);
        padding: 25px;
        border-radius: 20px;
        border: 3px solid {COLOR_DESTACADO};
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }}
    .ficha-jugador:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(255,167,38,0.3);
    }}
    
    /* Nombres y títulos */
    .nombre-jugador {{
        color: {COLOR_DESTACADO};
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .info-jugador {{
        color: {COLOR_SECUNDARIO};
        font-size: 18px;
        line-height: 1.6;
    }}
    
    /* Títulos principales */
    h1 {{
        color: {COLOR_DESTACADO} !important;
        font-size: 48px !important;
        font-weight: 800 !important;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin-bottom: 30px !important;
    }}
    h2 {{
        color: {COLOR_SECUNDARIO} !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        border-bottom: 3px solid {COLOR_DESTACADO};
        padding-bottom: 10px;
        margin-top: 30px !important;
    }}
    h3 {{
        color: {COLOR_ACENTO_1} !important;
        font-size: 24px !important;
        font-weight: 600 !important;
    }}
    
    /* Botones mejorados */
    .stButton > button {{
        background: linear-gradient(145deg, {COLOR_SECUNDARIO} 0%, {COLOR_ACENTO_1} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(30,136,229,0.5);
        background: linear-gradient(145deg, {COLOR_ACENTO_1} 0%, {COLOR_SECUNDARIO} 100%);
    }}
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: {COLOR_ACENTO_2};
        padding: 10px;
        border-radius: 15px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 10px;
        color: {COLOR_SECUNDARIO};
        font-weight: 600;
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(145deg, {COLOR_DESTACADO} 0%, {COLOR_ADVERTENCIA} 100%);
        color: {COLOR_PRIMARIO} !important;
    }}
    
    /* DataFrames mejorados */
    .stDataFrame {{
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    
    /* Selectbox y inputs */
    .stSelectbox, .stNumberInput, .stTextInput {{
        background-color: {COLOR_ACENTO_2};
        border-radius: 10px;
    }}
    
    /* Sidebar mejorado */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%);
        border-right: 2px solid {COLOR_DESTACADO};
    }}
    
    /* Alertas mejoradas */
    .stAlert {{
        border-radius: 12px;
        border-left: 5px solid {COLOR_DESTACADO};
    }}
</style>
""", unsafe_allow_html=True)

# URLS DE LA API
# Si está en Docker, usa la variable de entorno API_BASE_URL
# Si está en desarrollo local, usa localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_URL_FILTROS = f"{API_BASE_URL}/jugadores/filtros"
API_URL_BUSCAR = f"{API_BASE_URL}/jugadores/buscar"
API_URL_PERFIL = f"{API_BASE_URL}/jugadores/{{id}}/perfil"
API_URL_PREDECIR = f"{API_BASE_URL}/ml/predecir_valor"
API_URL_INFRAVALORADOS = f"{API_BASE_URL}/jugadores/infravalorados"
API_URL_SOBREVALORADOS = f"{API_BASE_URL}/jugadores/sobrevalorados"
API_URL_STATS = f"{API_BASE_URL}/eda/estadisticas_generales"
API_URL_GRAFICOS = f"{API_BASE_URL}/eda/datos_graficos"

# CONFIGURAR SESIÓN HTTP CON REINTENTOS
def crear_sesion_http():
    """Crea una sesión HTTP con reintentos automáticos"""
    sesion = requests.Session()
    reintentos = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adaptador = HTTPAdapter(max_retries=reintentos)
    sesion.mount("http://", adaptador)
    sesion.mount("https://", adaptador)
    return sesion

# Crear sesión global
sesion_http = crear_sesion_http()

# FUNCIONES DE CARGA DE DATOS
@st.cache_data(ttl=300)
def cargar_opciones_filtros():
    """Carga las opciones de filtros desde la API"""
    try:
        response = sesion_http.get(API_URL_FILTROS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar filtros: {e}")
        return None

@st.cache_data(ttl=60)
def buscar_jugadores(params):
    """Busca jugadores según filtros"""
    try:
        response = sesion_http.get(API_URL_BUSCAR, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al buscar jugadores: {e}")
        return None

def obtener_perfil_jugador(jugador_id):
    """Obtiene el perfil completo de un jugador"""
    try:
        url = API_URL_PERFIL.format(id=jugador_id)
        response = sesion_http.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener perfil: {e}")
        return None

@st.cache_data(ttl=300)
def cargar_estadisticas_generales():
    """Carga estadísticas generales del dataset"""
    try:
        response = sesion_http.get(API_URL_STATS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar estadísticas: {e}")
        return None

@st.cache_data(ttl=300)
def cargar_datos_graficos(tipo_analisis, top_n=20):
    """Carga datos para gráficos"""
    try:
        params = {"tipo_analisis": tipo_analisis, "top_n": top_n}
        response = sesion_http.get(API_URL_GRAFICOS, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos de gráficos: {e}")
        return None

def crear_grafico_radar(jugador_data):
    """Crea un gráfico de radar (araña) con los atributos del jugador"""
    
    # Atributos principales para el radar
    atributos = {
        "Ritmo": jugador_data.get("ritmo_velocidad", 0),
        "Tiro": jugador_data.get("tiro_disparo", 0),
        "Pase": jugador_data.get("pase", 0),
        "Regate": jugador_data.get("regate_gambeta", 0),
        "Defensa": jugador_data.get("defensa", 0),
        "Físico": jugador_data.get("fisico", 0)
    }
    
    categorias = list(atributos.keys())
    valores = list(atributos.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Atributos',
        line_color=COLOR_DESTACADO,
        fillcolor=COLOR_DESTACADO,
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=COLOR_SECUNDARIO,
                tickfont=dict(color=COLOR_SECUNDARIO)
            ),
            angularaxis=dict(
                gridcolor=COLOR_SECUNDARIO,
                tickfont=dict(color=COLOR_SECUNDARIO)
            ),
            bgcolor=COLOR_ACENTO_2
        ),
        showlegend=False,
        paper_bgcolor=COLOR_ACENTO_2,
        plot_bgcolor=COLOR_ACENTO_2,
        height=400
    )
    
    return fig

def obtener_imagen_jugador_fallback():
    """
    Retorna URL de imagen genérica de jugador de fútbol
    Usa placeholder con ícono de jugador (PNG compatible)
    """
    # Imagen placeholder con silueta de jugador de fútbol (PNG, siempre disponible)
    # Alternativas confiables:
    return "https://cdn-icons-png.flaticon.com/512/3774/3774299.png"

def obtener_bandera_pais(nacionalidad):
    """
    Genera URL de bandera del país del jugador
    API gratuita: Flagpedia (sin límites, sin auth)
    
    Args:
        nacionalidad: País del jugador
    
    Returns:
        Tuple (url_bandera_pequeña, nombre_pais)
    """
    # Mapeo de países a códigos ISO 3166-1 alpha-2
    paises_iso = {
        'Argentina': 'ar', 'Brazil': 'br', 'Spain': 'es', 'Germany': 'de',
        'France': 'fr', 'England': 'gb-eng', 'Italy': 'it', 'Portugal': 'pt',
        'Netherlands': 'nl', 'Belgium': 'be', 'Croatia': 'hr', 'Uruguay': 'uy',
        'Colombia': 'co', 'Chile': 'cl', 'Mexico': 'mx', 'Poland': 'pl',
        'Denmark': 'dk', 'Sweden': 'se', 'Norway': 'no', 'Austria': 'at',
        'Switzerland': 'ch', 'Czech Republic': 'cz', 'Turkey': 'tr', 'Greece': 'gr',
        'Russia': 'ru', 'Ukraine': 'ua', 'Serbia': 'rs', 'Scotland': 'gb-sct',
        'Wales': 'gb-wls', 'Republic of Ireland': 'ie', 'Northern Ireland': 'gb-nir',
        'Japan': 'jp', 'Korea Republic': 'kr', 'Australia': 'au', 'China PR': 'cn',
        'United States': 'us', 'Canada': 'ca', 'Egypt': 'eg', 'Morocco': 'ma',
        'Algeria': 'dz', 'Nigeria': 'ng', 'Senegal': 'sn', 'Ghana': 'gh',
        'Cameroon': 'cm', 'Ivory Coast': 'ci', 'South Africa': 'za', 'Ecuador': 'ec',
        'Peru': 'pe', 'Paraguay': 'py', 'Venezuela': 've', 'Bolivia': 'bo',
        'Costa Rica': 'cr', 'Iceland': 'is', 'Finland': 'fi', 'Romania': 'ro',
        'Hungary': 'hu', 'Slovakia': 'sk', 'Slovenia': 'si', 'Bosnia Herzegovina': 'ba',
        'Albania': 'al', 'North Macedonia': 'mk', 'Montenegro': 'me', 'Bulgaria': 'bg'
    }
    
    # Obtener código ISO del país
    codigo_pais = paises_iso.get(nacionalidad, 'un')  # 'un' = United Nations (bandera genérica)
    
    # URL de bandera pequeña para mostrar en el caption (80x60px)
    url_bandera = f"https://flagcdn.com/80x60/{codigo_pais}.png"
    
    return url_bandera, nacionalidad

def mostrar_ficha_jugador(jugador_id, jugador_nombre):
    """Muestra la ficha detallada de un jugador con gráfico radar"""
    
    perfil = obtener_perfil_jugador(jugador_id)
    
    if perfil and "jugador" in perfil:
        jugador = perfil["jugador"]
        prediccion = perfil.get("prediccion_ml", {})
        
        st.markdown(f"""
        <div class="ficha-jugador">
            <div class="nombre-jugador">{jugador.get('nombre_corto', 'N/A')}</div>
            <div class="info-jugador">
                {jugador.get('club', 'Sin club')} | {jugador.get('nacionalidad', 'N/A')} | {jugador.get('edad', 'N/A')} años
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            # Foto del jugador con fallback a ícono de jugador
            url_foto = jugador.get("url_foto_jugador", "")
            nacionalidad = jugador.get("nacionalidad", "")
            nombre = jugador.get("nombre_corto", "")
            
            if url_foto:
                try:
                    st.image(url_foto, width=200, caption=f"📸 {nombre}")
                except:
                    # Si falla la foto, usar ícono de jugador genérico con bandera superpuesta
                    url_jugador = obtener_imagen_jugador_fallback()
                    url_bandera, pais = obtener_bandera_pais(nacionalidad)
                    st.markdown(f"""
                    <div style='position: relative; width: 200px; margin: 0 auto;'>
                        <img src='{url_jugador}' style='width: 100%; height: auto; display: block; border-radius: 10px;'/>
                        <img src='{url_bandera}' style='position: absolute; bottom: 8px; right: 8px; width: 40px; height: auto; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'/>
                    </div>
                    <p style='text-align: center; margin-top: 5px; font-size: 0.9em;'>⚽ {pais}</p>
                    """, unsafe_allow_html=True)
            else:
                # Mostrar ícono de jugador genérico con bandera superpuesta
                url_jugador = obtener_imagen_jugador_fallback()
                url_bandera, pais = obtener_bandera_pais(nacionalidad)
                st.markdown(f"""
                <div style='position: relative; width: 200px; margin: 0 auto;'>
                    <img src='{url_jugador}' style='width: 100%; height: auto; display: block; border-radius: 10px;'/>
                    <img src='{url_bandera}' style='position: absolute; bottom: 8px; right: 8px; width: 40px; height: auto; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'/>
                </div>
                <p style='text-align: center; margin-top: 5px; font-size: 0.9em;'>⚽ {pais}</p>
                """, unsafe_allow_html=True)
            
            # Información básica
            st.markdown("##### Información")
            st.write(f"**Posición:** {jugador.get('posiciones_jugador', 'N/A')}")
            st.write(f"**Valoración:** {jugador.get('valoracion_global', 'N/A')}")
            st.write(f"**Potencial:** {jugador.get('potencial', 'N/A')}")
            st.write(f"**Pie:** {jugador.get('pie_preferido', 'N/A')}")
            st.write(f"**Liga:** {jugador.get('liga', 'N/A')}")
        
        with col2:
            # Gráfico de radar con atributos
            st.markdown("##### Atributos Técnicos")
            fig_radar = crear_grafico_radar(jugador)
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col3:
            # Comparación valor real vs predicho
            st.markdown("##### Análisis de Valor de Mercado")
            
            valor_real = jugador.get("valor_mercado_eur", 0)
            valor_predicho = prediccion.get("valor_predicho_eur", 0)
            diferencia = prediccion.get("diferencia_porcentual", 0)
            clasificacion = prediccion.get("clasificacion", "N/A")
            
            # Métricas
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Valor Real", f"€{valor_real:,.0f}")
            with col_m2:
                st.metric("Valor Predicho", f"€{valor_predicho:,.0f}")
            
            # Gráfico de comparación
            fig_comp = go.Figure()
            
            fig_comp.add_trace(go.Bar(
                x=["Valor Real", "Valor Predicho"],
                y=[valor_real, valor_predicho],
                marker_color=[COLOR_ACENTO_1, COLOR_DESTACADO],
                text=[f"€{valor_real:,.0f}", f"€{valor_predicho:,.0f}"],
                textposition='auto'
            ))
            
            fig_comp.update_layout(
                title="Comparación de Valores",
                yaxis_title="Euros (€)",
                showlegend=False,
                paper_bgcolor=COLOR_ACENTO_2,
                plot_bgcolor=COLOR_ACENTO_2,
                font=dict(color=COLOR_SECUNDARIO),
                height=300
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Clasificación
            if diferencia > 15:
                st.success(f"✓ {clasificacion} (+{diferencia:.1f}%)")
                st.info("Jugador potencialmente INFRAVALORADO")
            elif diferencia < -15:
                st.warning(f"⚠ {clasificacion} ({diferencia:.1f}%)")
                st.info("Jugador potencialmente SOBREVALORADO")
            else:
                st.info(f"• {clasificacion} ({diferencia:.1f}%)")
        
        # Atributos detallados
        st.markdown("---")
        st.markdown("##### Atributos Detallados")
        
        col_a1, col_a2, col_a3, col_a4 = st.columns(4)
        
        with col_a1:
            st.write("**Ataque**")
            st.write(f"Definición: {jugador.get('ataque_definicion', 'N/A')}")
            st.write(f"Cabezazo: {jugador.get('ataque_cabezazo', 'N/A')}")
            st.write(f"Voleas: {jugador.get('ataque_voleas', 'N/A')}")
        
        with col_a2:
            st.write("**Movimiento**")
            st.write(f"Aceleración: {jugador.get('movimiento_aceleracion', 'N/A')}")
            st.write(f"Sprint: {jugador.get('movimiento_velocidad_sprint', 'N/A')}")
            st.write(f"Agilidad: {jugador.get('movimiento_agilidad', 'N/A')}")
        
        with col_a3:
            st.write("**Mentalidad**")
            st.write(f"Visión: {jugador.get('mentalidad_vision', 'N/A')}")
            st.write(f"Compostura: {jugador.get('mentalidad_compostura', 'N/A')}")
            st.write(f"Agresividad: {jugador.get('mentalidad_agresividad', 'N/A')}")
        
        with col_a4:
            st.write("**Habilidades**")
            st.write(f"Control de balón: {jugador.get('habilidad_control_balon', 'N/A')}")
            st.write(f"Regate: {jugador.get('habilidad_regate', 'N/A')}")
            st.write(f"Pie débil: {jugador.get('pie_debil', 'N/A')} ⭐")

# ============================================================================
# FUNCIÓN MODAL DE FICHA DE JUGADOR
# ============================================================================
@st.dialog("📋 Ficha Detallada del Jugador", width="large")
def mostrar_modal_jugador(jugador_id, jugador_nombre, año_fifa):
    """Muestra la ficha del jugador en un modal interactivo"""
    
    # Header del modal
    st.markdown(f"### {jugador_nombre}")
    st.markdown(f"**📅 FIFA {año_fifa}**")
    st.markdown("---")
    
    # Cargar perfil del jugador
    perfil = obtener_perfil_jugador(jugador_id)
    
    if perfil and "jugador" in perfil:
        jugador = perfil["jugador"]
        prediccion = perfil.get("prediccion_ml", {})
        
        # SECCIÓN 1: INFO BÁSICA + FOTO
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Foto del jugador con fallback a ícono de jugador
            url_foto = jugador.get("url_foto_jugador", "")
            nacionalidad = jugador.get("nacionalidad", "")
            nombre = jugador.get("nombre_corto", "")
            
            if url_foto:
                try:
                    st.image(url_foto, width=250, caption=f"📸 {nombre}")
                except:
                    # Si falla la foto, usar ícono de jugador genérico con bandera superpuesta
                    url_jugador = obtener_imagen_jugador_fallback()
                    url_bandera, pais = obtener_bandera_pais(nacionalidad)
                    st.markdown(f"""
                    <div style='position: relative; width: 250px; margin: 0 auto;'>
                        <img src='{url_jugador}' style='width: 100%; height: auto; display: block; border-radius: 10px;'/>
                        <img src='{url_bandera}' style='position: absolute; bottom: 10px; right: 10px; width: 50px; height: auto; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.4);'/>
                    </div>
                    <p style='text-align: center; margin-top: 8px; font-size: 0.95em;'>⚽ {pais} • Foto no disponible</p>
                    """, unsafe_allow_html=True)
            else:
                # Mostrar ícono de jugador genérico con bandera superpuesta
                url_jugador = obtener_imagen_jugador_fallback()
                url_bandera, pais = obtener_bandera_pais(nacionalidad)
                st.markdown(f"""
                <div style='position: relative; width: 250px; margin: 0 auto;'>
                    <img src='{url_jugador}' style='width: 100%; height: auto; display: block; border-radius: 10px;'/>
                    <img src='{url_bandera}' style='position: absolute; bottom: 10px; right: 10px; width: 50px; height: auto; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.4);'/>
                </div>
                <p style='text-align: center; margin-top: 8px; font-size: 0.95em;'>⚽ {pais} • Foto no disponible</p>
                """, unsafe_allow_html=True)
            
            # Info básica en tarjetas
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%); 
                 padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {COLOR_ACENTO_1};'>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>🏟️ Club:</b> {jugador.get('club', 'N/A')}</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>🏆 Liga:</b> {jugador.get('liga', 'N/A')}</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>🌍 Nacionalidad:</b> {jugador.get('nacionalidad', 'N/A')}</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>🎂 Edad:</b> {jugador.get('edad', 'N/A')} años</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>📅 Año FIFA:</b> {año_fifa}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas principales
            st.markdown("#### ⚡ Métricas Clave")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("⚽ Overall", jugador.get('valoracion_global', 'N/A'))
                st.metric("🦵 Pie", jugador.get('pie_preferido', 'N/A'))
            with col_m2:
                st.metric("🚀 Potencial", jugador.get('potencial', 'N/A'))
                st.metric("📍 Posición", jugador.get('posiciones_jugador', 'N/A'))
        
        with col2:
            # Tabs para organizar información
            tab1, tab2, tab3 = st.tabs(["📊 Atributos", "💰 Valoración", "📈 Estadísticas"])
            
            with tab1:
                # Gráfico de radar
                st.markdown("##### Perfil de Habilidades")
                fig_radar = crear_grafico_radar(jugador)
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Atributos detallados en 3 columnas
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    st.markdown("**⚔️ Ataque**")
                    st.progress(int(jugador.get('ataque_definicion', 0)) / 100)
                    st.caption(f"Definición: {jugador.get('ataque_definicion', 'N/A')}")
                    st.progress(int(jugador.get('ataque_cabezazo', 0)) / 100)
                    st.caption(f"Cabezazo: {jugador.get('ataque_cabezazo', 'N/A')}")
                
                with col_a2:
                    st.markdown("**🏃 Movimiento**")
                    st.progress(int(jugador.get('movimiento_aceleracion', 0)) / 100)
                    st.caption(f"Aceleración: {jugador.get('movimiento_aceleracion', 'N/A')}")
                    st.progress(int(jugador.get('movimiento_velocidad_sprint', 0)) / 100)
                    st.caption(f"Sprint: {jugador.get('movimiento_velocidad_sprint', 'N/A')}")
                
                with col_a3:
                    st.markdown("**🧠 Mentalidad**")
                    st.progress(int(jugador.get('mentalidad_vision', 0)) / 100)
                    st.caption(f"Visión: {jugador.get('mentalidad_vision', 'N/A')}")
                    st.progress(int(jugador.get('mentalidad_compostura', 0)) / 100)
                    st.caption(f"Compostura: {jugador.get('mentalidad_compostura', 'N/A')}")
            
            with tab2:
                # Análisis de valor de mercado
                st.markdown("##### 💰 Análisis de Valor de Mercado")
                
                valor_real = jugador.get("valor_mercado_eur", 0)
                valor_predicho = prediccion.get("valor_predicho_eur", 0)
                diferencia = prediccion.get("diferencia_porcentual", 0)
                clasificacion = prediccion.get("clasificacion", "N/A")
                
                # Métricas lado a lado
                col_v1, col_v2, col_v3 = st.columns(3)
                with col_v1:
                    st.metric("💵 Valor Real", f"€{valor_real:,.0f}")
                with col_v2:
                    st.metric("🤖 Valor Predicho", f"€{valor_predicho:,.0f}")
                with col_v3:
                    delta_valor = valor_real - valor_predicho
                    st.metric("📊 Diferencia", f"€{delta_valor:,.0f}", delta=f"{diferencia:.1f}%")
                
                # Gráfico de comparación
                fig_comp = go.Figure()
                
                fig_comp.add_trace(go.Bar(
                    x=["Valor Real", "Valor Predicho ML"],
                    y=[valor_real, valor_predicho],
                    marker_color=[COLOR_ACENTO_1, COLOR_DESTACADO],
                    text=[f"€{valor_real:,.0f}", f"€{valor_predicho:,.0f}"],
                    textposition='auto',
                    textfont=dict(size=14, color='white')
                ))
                
                fig_comp.update_layout(
                    title="Comparación: Real vs Predicción",
                    yaxis_title="Euros (€)",
                    showlegend=False,
                    paper_bgcolor=COLOR_ACENTO_2,
                    plot_bgcolor=COLOR_ACENTO_2,
                    font=dict(color=COLOR_SECUNDARIO),
                    height=300
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
                
                # Clasificación con badge
                if diferencia > 15:
                    st.success(f"✅ **{clasificacion}** (+{diferencia:.1f}%)")
                    st.info("🔍 **Oportunidad:** Jugador potencialmente INFRAVALORADO")
                elif diferencia < -15:
                    st.warning(f"⚠️ **{clasificacion}** ({diferencia:.1f}%)")
                    st.info("💡 **Alerta:** Jugador potencialmente SOBREVALORADO")
                else:
                    st.info(f"✓ **{clasificacion}** ({diferencia:.1f}%)")
                    st.caption("Valoración acorde al mercado")
            
            with tab3:
                # Estadísticas adicionales
                st.markdown("##### 📈 Estadísticas Físicas y Técnicas")
                
                col_s1, col_s2 = st.columns(2)
                
                with col_s1:
                    st.markdown("**Físico**")
                    st.write(f"📏 Altura: {jugador.get('altura_cm', 'N/A')} cm")
                    st.write(f"⚖️ Peso: {jugador.get('peso_kg', 'N/A')} kg")
                    st.write(f"💪 Fuerza: {jugador.get('poder_fuerza', 'N/A')}")
                    st.write(f"⏱️ Resistencia: {jugador.get('poder_resistencia', 'N/A')}")
                
                with col_s2:
                    st.markdown("**Técnica**")
                    st.write(f"⚽ Control: {jugador.get('habilidad_control_balon', 'N/A')}")
                    st.write(f"🎯 Regate: {jugador.get('habilidad_regate', 'N/A')}")
                    st.write(f"🦶 Pie débil: {jugador.get('pie_debil', 'N/A')} ⭐")
                    st.write(f"✨ Habilidades: {jugador.get('movimientos_habilidad', 'N/A')} ⭐")
                
                # Información contractual
                st.markdown("---")
                st.markdown("**💼 Información Contractual**")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    salario = jugador.get('salario_eur', 0)
                    st.write(f"💰 Salario: €{salario:,.0f}")
                with col_c2:
                    st.write(f"📋 Cláusula: €{jugador.get('clausula_rescision_eur', 0):,.0f}")
    
    else:
        st.error("❌ No se pudo cargar la información del jugador")
        st.info("Intenta refrescar la página o selecciona otro jugador")

# ============================================================================
# HEADER PRINCIPAL MEJORADO
# ============================================================================
st.markdown(f"""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, {COLOR_ACENTO_1} 100%); border-radius: 20px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
    <h1 style='color: white; font-size: 56px; margin: 0; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);'>
        ⚽ FIFA SCOUTING PRO
    </h1>
    <p style='color: rgba(255,255,255,0.9); font-size: 20px; margin: 15px 0; font-weight: 500;'>
        Sistema Inteligente de Análisis y Valoración de Jugadores
    </p>
    <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-top: 20px;'>
        <div style='background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; backdrop-filter: blur(10px);'>
            <span style='color: white; font-weight: 600;'>🤖 Machine Learning</span>
        </div>
        <div style='background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; backdrop-filter: blur(10px);'>
            <span style='color: white; font-weight: 600;'>📊 122,501 Jugadores</span>
        </div>
        <div style='background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; backdrop-filter: blur(10px);'>
            <span style='color: white; font-weight: 600;'>🎯 Random Forest</span>
        </div>
    </div>
    <p style='color: rgba(255,255,255,0.7); font-size: 14px; margin-top: 20px; font-style: italic;'>
        Universidad Regional Autónoma de los Andes (UniAndes) | Seminario Complexivo | Prof. Juan Felipe Nájera
    </p>
</div>
""", unsafe_allow_html=True)

# CREAR PESTAÑAS CON DISEÑO MEJORADO
tab1, tab2, tab3 = st.tabs([
    "🔍  Búsqueda Inteligente",
    "📊  Análisis de Mercado",
    "🤖  Predicción ML"
])

# Cargar opciones de filtros
data_filtros = cargar_opciones_filtros()

if data_filtros and "error" not in data_filtros:
    posiciones_lista = data_filtros.get("posiciones", [])
    nacionalidades_lista = data_filtros.get("nacionalidades", [])
    clubes_lista = data_filtros.get("clubes", [])
    ligas_lista = data_filtros.get("ligas", [])
    categorias_edad = data_filtros.get("categorias_edad", [])
else:
    st.error("No se pudieron cargar los filtros desde la API")
    posiciones_lista = []
    nacionalidades_lista = []
    clubes_lista = []
    ligas_lista = []
    categorias_edad = []

# ============================================================================
# TAB 1: BÚSQUEDA INTELIGENTE
# ============================================================================
with tab1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%); 
         padding: 20px; border-radius: 15px; border-left: 5px solid {COLOR_DESTACADO}; margin-bottom: 25px;'>
        <h2 style='color: {COLOR_DESTACADO}; margin: 0;'>🔍 Búsqueda Inteligente de Jugadores</h2>
        <p style='color: {COLOR_SECUNDARIO}; margin: 10px 0 0 0;'>
            Encuentra jugadores usando filtros avanzados y visualiza estadísticas detalladas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS GLOBAL PARA FORZAR COLORES EN SIDEBAR
    st.markdown("""
    <style>
        /* Forzar color blanco en título de filtros */
        [data-testid="stSidebar"] h2 {
            color: white !important;
        }
        
        /* Asegurar que el div contenedor no interfiera */
        [data-testid="stSidebar"] div h2 {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # FILTROS EN SIDEBAR MEJORADO
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, {COLOR_ACENTO_1} 100%); border-radius: 15px; margin-bottom: 20px;'>
            <h2 style='color: white !important; margin: 0;'>🎯 Filtros Avanzados</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # ⚽ FILTRO DE AÑO FIFA (NUEVO)
        st.markdown("### 📅 Año FIFA")
        año_filtro = st.selectbox(
            "Selecciona el año:",
            options=["Todos", 2021, 2020, 2019, 2018, 2017, 2016, 2015],
            index=1,  # Por defecto 2021
            help="Por defecto muestra solo jugadores de 2021 (versión más reciente)"
        )
        
        st.markdown("---")  # Separador visual
        
        # Filtro de posiciones
        posiciones_seleccionadas = st.multiselect(
            "Posiciones:",
            options=posiciones_lista[:50],  # Top 50 posiciones
            default=None
        )
        
        # Filtro de nacionalidades
        nacionalidades_seleccionadas = st.multiselect(
            "Nacionalidades:",
            options=nacionalidades_lista[:30],  # Top 30
            default=None
        )
        
        # Filtro de edad
        edad_min = st.slider("Edad mínima:", 16, 45, 18)
        edad_max = st.slider("Edad máxima:", 16, 45, 35)
        
        # Filtro de valoración
        overall_min = st.slider("Valoración mínima:", 40, 95, 70)
        
        # Filtro de potencial
        potencial_min = st.slider("Potencial mínimo:", 40, 95, 70)
        
        # Filtro de valor de mercado
        valor_max_millones = st.number_input(
            "Valor máximo (millones €):",
            min_value=0.0,
            max_value=200.0,
            value=50.0,
            step=5.0
        )
        
        # Ordenamiento
        ordenar_por = st.selectbox(
            "Ordenar por:",
            options=["valor_mercado_eur", "valoracion_global", "potencial", "edad"],
            format_func=lambda x: {
                "valor_mercado_eur": "Valor de mercado",
                "valoracion_global": "Valoración",
                "potencial": "Potencial",
                "edad": "Edad"
            }[x]
        )
        
        orden_desc = st.checkbox("Orden descendente", value=True)
        
        limite_resultados = st.slider("Máximo de resultados:", 10, 100, 20)
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_buscar = st.button("🔍 Buscar Jugadores", type="primary", use_container_width=True)
        
        # Info adicional
        st.markdown(f"""
        <div style='margin-top: 20px; padding: 15px; background: rgba({int(COLOR_ACENTO_1[1:3],16)}, {int(COLOR_ACENTO_1[3:5],16)}, {int(COLOR_ACENTO_1[5:7],16)}, 0.2); border-radius: 10px; border-left: 3px solid {COLOR_ACENTO_1};'>
            <p style='color: {COLOR_SECUNDARIO}; font-size: 12px; margin: 0;'>
                💡 <b>Tip:</b> Deja filtros vacíos para buscar en todo el dataset (122,501 jugadores)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # RESULTADOS DE BÚSQUEDA
    if btn_buscar or "resultados_busqueda" not in st.session_state:
        
        # Construir parámetros
        params = {
            "limite": limite_resultados,
            "ordenar_por": ordenar_por,
            "orden_descendente": orden_desc
        }
        
        # ⚽ FILTRO DE AÑO (NUEVO)
        if año_filtro != "Todos":
            params["año_datos"] = año_filtro
        
        if posiciones_seleccionadas:
            params["posiciones_jugador"] = posiciones_seleccionadas
        if nacionalidades_seleccionadas:
            params["nacionalidad"] = nacionalidades_seleccionadas
        if edad_min:
            params["edad_min"] = edad_min
        if edad_max:
            params["edad_max"] = edad_max
        if overall_min:
            params["valoracion_global_min"] = overall_min
        if potencial_min:
            params["potencial_min"] = potencial_min
        if valor_max_millones:
            params["valor_mercado_max_eur"] = valor_max_millones * 1_000_000
        
        # Buscar jugadores
        resultados = buscar_jugadores(params)
        st.session_state.resultados_busqueda = resultados
    else:
        resultados = st.session_state.resultados_busqueda
    
    # Mostrar resultados
    if resultados:
        jugadores = resultados.get("jugadores", [])
        total_encontrados = resultados.get("total_encontrados", 0)
        
        # KPIs
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Jugadores Encontrados", f"{total_encontrados:,}")
        
        if jugadores:
            valor_total = sum([j.get("valor_mercado_eur", 0) for j in jugadores])
            edad_promedio = sum([j.get("edad", 0) for j in jugadores]) / len(jugadores)
            valoracion_promedio = sum([j.get("valoracion_global", 0) for j in jugadores]) / len(jugadores)
            
            with col2:
                st.metric("Valor Total", f"€{valor_total:,.0f}")
            with col3:
                st.metric("Edad Promedio", f"{edad_promedio:.1f} años")
            with col4:
                st.metric("Valoración Promedio", f"{valoracion_promedio:.1f}")
        
        st.markdown("---")
        
        # TABLA DE RESULTADOS
        if jugadores:
            st.subheader(f"Resultados: {len(jugadores)} jugadores")
            
            # Convertir a DataFrame para mejor visualización
            df_resultados = pd.DataFrame(jugadores)
            
            # Seleccionar columnas relevantes
            columnas_mostrar = [
                "nombre_corto", "edad", "nacionalidad", "club", "liga",
                "posiciones_jugador", "valoracion_global", "potencial",
                "valor_mercado_eur"
            ]
            
            # ⚽ Agregar columna año_datos si existe
            if "año_datos" in df_resultados.columns:
                columnas_mostrar.insert(2, "año_datos")
            
            df_mostrar = df_resultados[columnas_mostrar].copy()
            
            # Renombrar columnas
            columnas_renombradas = [
                "Nombre", "Edad", "Año FIFA", "Nacionalidad", "Club", "Liga",
                "Posición", "Overall", "Potencial", "Valor (€)"
            ] if "año_datos" in df_resultados.columns else [
                "Nombre", "Edad", "Nacionalidad", "Club", "Liga",
                "Posición", "Overall", "Potencial", "Valor (€)"
            ]
            
            df_mostrar.columns = columnas_renombradas
            
            # Formatear valor
            df_mostrar["Valor (€)"] = df_mostrar["Valor (€)"].apply(lambda x: f"€{x:,.0f}")
            
            # Agregar columna de numeración estática
            df_mostrar.insert(0, '#', range(1, len(df_mostrar) + 1))
            
            # PAGINACIÓN - 20 jugadores por página
            jugadores_por_pagina = 20
            total_paginas = (len(jugadores) - 1) // jugadores_por_pagina + 1
            
            # Inicializar página actual en session state si no existe
            if 'pagina_actual' not in st.session_state:
                st.session_state.pagina_actual = 1
            
            # Controles de paginación
            col_pag1, col_pag2, col_pag3 = st.columns([2, 6, 2])
            
            with col_pag1:
                if st.button("⬅️ Anterior", disabled=(st.session_state.pagina_actual == 1)):
                    st.session_state.pagina_actual -= 1
                    st.rerun()
            
            with col_pag2:
                st.markdown(f"<h4 style='text-align: center;'>Página {st.session_state.pagina_actual} de {total_paginas}</h4>", unsafe_allow_html=True)
            
            with col_pag3:
                if st.button("Siguiente ➡️", disabled=(st.session_state.pagina_actual == total_paginas)):
                    st.session_state.pagina_actual += 1
                    st.rerun()
            
            st.markdown("---")
            
            # Calcular índices de inicio y fin para la página actual
            inicio = (st.session_state.pagina_actual - 1) * jugadores_por_pagina
            fin = min(inicio + jugadores_por_pagina, len(jugadores))
            jugadores_pagina = jugadores[inicio:fin]
            
            # CREAR TABLA PERSONALIZADA CON DISEÑO MEJORADO
            # CSS mejorado para la tabla con diseño moderno y responsive
            st.markdown("""
            <style>
                /* Estilos generales de la tabla */
                .tabla-header {
                    background: linear-gradient(135deg, #304878 0%, #1a2844 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    font-weight: bold;
                    color: #f0a818;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                
                .fila-jugador {
                    background: linear-gradient(135deg, #181848 0%, #0f0f2e 100%);
                    padding: 12px;
                    margin: 8px 0;
                    border-radius: 10px;
                    border-left: 4px solid #7890a8;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }
                
                .fila-jugador:hover {
                    background: linear-gradient(135deg, #304878 0%, #1e2d52 100%);
                    border-left: 4px solid #f0a818;
                    transform: translateX(5px);
                    box-shadow: 0 4px 12px rgba(240, 168, 24, 0.3);
                }
                
                .jugador-nombre {
                    color: #f0a818;
                    font-weight: bold;
                    font-size: 1.1em;
                }
                
                .jugador-stat {
                    color: #7890a8;
                    padding: 4px 8px;
                    background-color: rgba(48, 72, 120, 0.3);
                    border-radius: 5px;
                    display: inline-block;
                    margin: 2px;
                }
                
                .overall-badge {
                    background: linear-gradient(135deg, #f0a818 0%, #d89510 100%);
                    color: #000;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-weight: bold;
                    display: inline-block;
                }
                
                /* Estilos para botones de paginación - Texto blanco */
                button[kind="primary"], button[kind="secondary"] {
                    color: white !important;
                }
                
                button p {
                    color: white !important;
                }
                
                /* Responsive - Vista de tarjetas en móvil */
                @media (max-width: 768px) {
                    .fila-jugador {
                        padding: 15px;
                        border-left: none;
                        border-top: 4px solid #7890a8;
                    }
                    
                    .fila-jugador:hover {
                        transform: translateY(-5px);
                        border-top: 4px solid #f0a818;
                    }
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Mostrar encabezados (con nueva columna Año FIFA)
            col_headers = st.columns([0.5, 1.2, 2, 0.7, 0.7, 1.5, 1.5, 1.5, 1, 1, 1.2])
            headers = ["#", "Acción", "Nombre", "Edad", "Año FIFA", "Nacionalidad", "Club", "Liga", "Posición", "Overall", "Potencial"]
            
            header_html = "<div class='tabla-header'>"
            for col, header in zip(col_headers, headers):
                with col:
                    st.markdown(f"**{header}**")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Mostrar cada fila con diseño mejorado
            for idx, jugador in enumerate(jugadores_pagina):
                idx_global = inicio + idx
                
                # Wrapper de fila con clase CSS
                st.markdown("<div class='fila-jugador'>", unsafe_allow_html=True)
                
                with st.container():
                    col_vals = st.columns([0.5, 1.2, 2.5, 0.7, 0.7, 1.5, 1.5, 1.5, 1, 1, 1])
                    
                    with col_vals[0]:
                        st.markdown(f"<div style='text-align: center; font-size: 1.2em; color: #f0a818; font-weight: bold;'>{idx_global + 1}</div>", unsafe_allow_html=True)
                    
                    with col_vals[1]:
                        jugador_id = jugador.get('id_sofifa')
                        nombre = jugador.get('nombre_corto', 'N/A')
                        año_jugador = jugador.get('año_datos', 'N/A')
                        # Modal: guardar info del jugador y marcar para mostrar modal
                        if st.button("🎯 Ficha", key=f"ficha_{idx_global}_{jugador_id}", help="Ver ficha completa del jugador", use_container_width=True):
                            st.session_state.modal_jugador_id = jugador_id
                            st.session_state.modal_jugador_nombre = nombre
                            st.session_state.modal_jugador_año = año_jugador
                            st.session_state.mostrar_modal = True
                            st.rerun()
                    
                    with col_vals[2]:
                        st.markdown(f"<span class='jugador-nombre'>{jugador.get('nombre_corto', 'N/A')}</span>", unsafe_allow_html=True)
                    
                    with col_vals[3]:
                        edad = jugador.get('edad', 'N/A')
                        st.markdown(f"<div style='text-align: center;'>{edad}</div>", unsafe_allow_html=True)
                    
                    with col_vals[4]:
                        # ⚽ NUEVA COLUMNA AÑO FIFA
                        año = jugador.get('año_datos', 'N/A')
                        st.markdown(f"<div style='text-align: center; background: linear-gradient(135deg, #f0a818 0%, #d89510 100%); color: #000; padding: 3px 8px; border-radius: 10px; font-weight: bold; font-size: 0.85em;'>{año}</div>", unsafe_allow_html=True)
                    
                    with col_vals[5]:
                        nacionalidad = jugador.get('nacionalidad', 'N/A')
                        st.markdown(f"<span class='jugador-stat'>{nacionalidad}</span>", unsafe_allow_html=True)
                    
                    with col_vals[6]:
                        club = jugador.get('club', 'N/A')
                        st.markdown(f"<div style='color: #7890a8;'>{club}</div>", unsafe_allow_html=True)
                    
                    with col_vals[7]:
                        liga = jugador.get('liga', 'N/A')
                        st.markdown(f"<div style='color: #7890a8; font-size: 0.9em;'>{liga}</div>", unsafe_allow_html=True)
                    
                    with col_vals[8]:
                        posicion = jugador.get('posiciones_jugador', 'N/A')
                        st.markdown(f"<div style='text-align: center; background-color: rgba(120, 144, 168, 0.2); padding: 4px; border-radius: 5px;'>{posicion}</div>", unsafe_allow_html=True)
                    
                    with col_vals[9]:
                        overall = jugador.get('valoracion_global', 'N/A')
                        st.markdown(f"<div class='overall-badge'>{overall}</div>", unsafe_allow_html=True)
                    
                    with col_vals[10]:
                        potencial = jugador.get('potencial', 'N/A')
                        color_potencial = "#4CAF50" if potencial > overall else "#FF9800"
                        st.markdown(f"<div style='text-align: center; color: {color_potencial}; font-weight: bold;'>{potencial}</div>", unsafe_allow_html=True)
                
                # Cerrar wrapper de fila
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Controles de paginación al final
            st.markdown("---")
            col_pag_fin1, col_pag_fin2, col_pag_fin3 = st.columns([2, 6, 2])
            
            with col_pag_fin1:
                if st.button("⬅️ Anterior ", disabled=(st.session_state.pagina_actual == 1), key="prev_bottom"):
                    st.session_state.pagina_actual -= 1
                    st.rerun()
            
            with col_pag_fin2:
                st.markdown(f"<h4 style='text-align: center;'>Mostrando {inicio + 1}-{fin} de {len(jugadores)} jugadores</h4>", unsafe_allow_html=True)
            
            with col_pag_fin3:
                if st.button("Siguiente ➡️ ", disabled=(st.session_state.pagina_actual == total_paginas), key="next_bottom"):
                    st.session_state.pagina_actual += 1
                    st.rerun()
            
            # ⚽ MODAL DE FICHA DE JUGADOR
            if st.session_state.get('mostrar_modal', False):
                mostrar_modal_jugador(
                    st.session_state.get('modal_jugador_id'),
                    st.session_state.get('modal_jugador_nombre', 'Jugador'),
                    st.session_state.get('modal_jugador_año', 'N/A')
                )
        else:
            st.info("No se encontraron jugadores con los criterios seleccionados")

# ============================================================================
# TAB 2: ANÁLISIS DE MERCADO
# ============================================================================
with tab2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%); 
         padding: 20px; border-radius: 15px; border-left: 5px solid {COLOR_ACENTO_1}; margin-bottom: 25px;'>
        <h2 style='color: {COLOR_ACENTO_1}; margin: 0;'>📊 Análisis Exploratorio del Mercado</h2>
        <p style='color: {COLOR_SECUNDARIO}; margin: 10px 0 0 0;'>
            Estadísticas globales, distribuciones y tendencias del mercado futbolístico
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar estadísticas generales
    stats = cargar_estadisticas_generales()
    
    if stats:
        # KPIs GENERALES CON DISEÑO MEJORADO
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h3 style='color: {COLOR_ACENTO_1};'>📈 Estadísticas Globales del Dataset</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "👥 Total Jugadores", 
                f"{stats.get('total_jugadores', 0):,}",
                delta="FIFA 2015-2021"
            )
        with col2:
            st.metric(
                "⚽ Total Clubes", 
                f"{stats.get('total_clubes', 0):,}",
                delta="Mundial"
            )
        with col3:
            st.metric(
                "🏆 Total Ligas", 
                f"{stats.get('total_ligas', 0):,}",
                delta="Profesionales"
            )
        with col4:
            st.metric(
                "📅 Edad Promedio", 
                f"{stats.get('edad_promedio', 0):.1f} años",
                delta="Edad ideal"
            )
        with col5:
            valor_promedio = stats.get('valor_mercado_promedio_eur', 0)
            st.metric(
                "💰 Valor Promedio", 
                f"€{valor_promedio/1_000_000:.1f}M",
                delta="Por jugador"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # JUGADOR MÁS VALIOSO CON DISEÑO DESTACADO
        jugador_top = stats.get("jugador_mas_valioso", {})
        if jugador_top:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {COLOR_DESTACADO} 0%, {COLOR_ADVERTENCIA} 100%); 
                 padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 8px 32px rgba(255,167,38,0.4);
                 margin: 20px 0;'>
                <h3 style='color: {COLOR_PRIMARIO}; margin: 0 0 15px 0;'>⭐ JUGADOR MÁS VALIOSO DEL DATASET</h3>
                <h2 style='color: white; font-size: 36px; margin: 10px 0;'>{jugador_top.get('nombre', 'N/A')}</h2>
                <p style='color: {COLOR_PRIMARIO}; font-size: 20px; font-weight: 600; margin: 10px 0;'>
                    🏆 {jugador_top.get('club', 'N/A')}
                </p>
                <p style='color: white; font-size: 28px; font-weight: bold; margin: 15px 0 0 0;'>
                    💰 €{jugador_top.get('valor_eur', 0)/1_000_000:.1f} Millones
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICOS
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Top 20 Clubes por Valor Total")
        datos_clubes = cargar_datos_graficos("clubes", 20)
        
        if datos_clubes and "datos" in datos_clubes:
            df_clubes = pd.DataFrame(datos_clubes["datos"])
            
            fig_clubes = px.bar(
                df_clubes,
                x="valor_total_eur",
                y="club",
                orientation="h",
                title="💰 Valor Total de Plantilla por Club",
                labels={"valor_total_eur": "Valor Total (€)", "club": "Club"},
                color="valor_total_eur",
                color_continuous_scale=["#1E88E5", "#00ACC1", "#FFA726", "#FDD835"],
                text_auto=".2s"
            )
            
            fig_clubes.update_layout(
                showlegend=False,
                paper_bgcolor=COLOR_PRIMARIO,
                plot_bgcolor=COLOR_ACENTO_2,
                font=dict(color="white", size=12),
                yaxis={'categoryorder':'total ascending'},
                title_font=dict(size=18, color=COLOR_DESTACADO, family="Arial Black"),
                margin=dict(l=10, r=10, t=50, b=10),
                hoverlabel=dict(bgcolor=COLOR_ACENTO_2, font_size=14)
            )
            
            st.plotly_chart(fig_clubes, use_container_width=True)
    
    with col_graf2:
        st.subheader("Top 20 Ligas por Valor Promedio")
        datos_ligas = cargar_datos_graficos("ligas", 20)
        
        if datos_ligas and "datos" in datos_ligas:
            df_ligas = pd.DataFrame(datos_ligas["datos"])
            
            fig_ligas = px.bar(
                df_ligas,
                x="valor_promedio_eur",
                y="liga",
                orientation="h",
                title="🏆 Valor Promedio por Liga",
                labels={"valor_promedio_eur": "Valor Promedio (€)", "liga": "Liga"},
                color="valor_promedio_eur",
                color_continuous_scale=["#00ACC1", "#1E88E5", "#66BB6A", "#FFA726"],
                text_auto=".2s"
            )
            
            fig_ligas.update_layout(
                showlegend=False,
                paper_bgcolor=COLOR_PRIMARIO,
                plot_bgcolor=COLOR_ACENTO_2,
                font=dict(color="white", size=12),
                yaxis={'categoryorder':'total ascending'},
                title_font=dict(size=18, color=COLOR_ACENTO_1, family="Arial Black"),
                margin=dict(l=10, r=10, t=50, b=10),
                hoverlabel=dict(bgcolor=COLOR_ACENTO_2, font_size=14)
            )
            
            st.plotly_chart(fig_ligas, use_container_width=True)
    
    st.markdown("---")
    
    # DISTRIBUCIÓN POR POSICIONES
    st.subheader("Distribución por Posiciones")
    datos_posiciones = cargar_datos_graficos("posiciones", 10)
    
    if datos_posiciones and "datos" in datos_posiciones:
        df_posiciones = pd.DataFrame(datos_posiciones["datos"])
        
        fig_posiciones = px.pie(
            df_posiciones,
            values="cantidad",
            names="categoria",
            title="Distribución de Jugadores por Posición",
            color_discrete_sequence=[COLOR_ACENTO_1, COLOR_ACENTO_2, COLOR_SECUNDARIO, COLOR_DESTACADO]
        )
        
        fig_posiciones.update_layout(
            paper_bgcolor=COLOR_ACENTO_2,
            font=dict(color=COLOR_SECUNDARIO)
        )
        
        st.plotly_chart(fig_posiciones, use_container_width=True)
    
    st.markdown("---")
    
    # OPORTUNIDADES DE MERCADO
    st.subheader("💎 Oportunidades de Mercado")
    
    col_oport1, col_oport2 = st.columns(2)
    
    with col_oport1:
        st.markdown("##### Jugadores Infravalorados")
        
        try:
            response_infra = sesion_http.get(API_URL_INFRAVALORADOS, params={"top": 10}, timeout=30)
            if response_infra.status_code == 200:
                data_infra = response_infra.json()
                jugadores_infra = data_infra.get("top_jugadores", [])
                
                if jugadores_infra:
                    for i, jug in enumerate(jugadores_infra[:5], 1):
                        st.write(f"{i}. **{jug.get('nombre_corto')}** ({jug.get('club')})")
                        st.write(f"   Real: €{jug.get('valor_mercado_eur', 0):,.0f} → Predicho: €{jug.get('valor_predicho_eur', 0):,.0f}")
                        st.write(f"   Diferencia: +{jug.get('diferencia_porcentual', 0):.1f}%")
                        st.markdown("---")
                else:
                    st.info("No hay jugadores infravalorados en este momento")
        except Exception as e:
            st.error(f"Error: {e}")
    
    with col_oport2:
        st.markdown("##### Jugadores Sobrevalorados")
        
        try:
            response_sobre = sesion_http.get(API_URL_SOBREVALORADOS, params={"top": 10}, timeout=30)
            if response_sobre.status_code == 200:
                data_sobre = response_sobre.json()
                jugadores_sobre = data_sobre.get("top_jugadores", [])
                
                if jugadores_sobre:
                    for i, jug in enumerate(jugadores_sobre[:5], 1):
                        st.write(f"{i}. **{jug.get('nombre_corto')}** ({jug.get('club')})")
                        st.write(f"   Real: €{jug.get('valor_mercado_eur', 0):,.0f} → Predicho: €{jug.get('valor_predicho_eur', 0):,.0f}")
                        st.write(f"   Diferencia: {jug.get('diferencia_porcentual', 0):.1f}%")
                        st.markdown("---")
                else:
                    st.info("No hay jugadores sobrevalorados en este momento")
        except Exception as e:
            st.error(f"Error: {e}")

# ============================================================================
# TAB 3: PREDICCIÓN DE VALOR
# ============================================================================
with tab3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%); 
         padding: 20px; border-radius: 15px; border-left: 5px solid {COLOR_EXITO}; margin-bottom: 25px;'>
        <h2 style='color: {COLOR_EXITO}; margin: 0;'>🤖 Predictor de Valor de Mercado con ML</h2>
        <p style='color: {COLOR_SECUNDARIO}; margin: 10px 0 0 0;'>
            🌲 Random Forest (4000 árboles) | 📊 R² = 0.65-0.98 | 🎯 84 features
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_inputs, col_resultado = st.columns([2, 1])
    
    with col_inputs:
        st.subheader("Parámetros del Jugador")
        
        with st.form("prediction_form"):
            
            st.markdown("##### Información Básica")
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                edad = st.slider("Edad:", 16, 45, 25)
                valoracion_global = st.slider("Valoración Global:", 40, 95, 75)
                potencial = st.slider("Potencial:", 40, 95, 80)
            
            with col_f2:
                pie_preferido = st.selectbox("Pie Preferido:", ["Right", "Left"])
                pie_debil = st.slider("Pie Débil (1-5):", 1, 5, 3)
                habilidades_regate = st.slider("Habilidades Regate (1-5):", 1, 5, 3)
            
            with col_f3:
                reputacion = st.slider("Reputación Internacional (1-5):", 1, 5, 3)
                anos_contrato = st.slider("Años de Contrato Restantes:", 0, 5, 2)
            
            st.markdown("---")
            st.markdown("##### Atributos Técnicos")
            
            col_t1, col_t2, col_t3, col_t4, col_t5, col_t6 = st.columns(6)
            
            with col_t1:
                ritmo = st.slider("Ritmo:", 0, 100, 70)
            with col_t2:
                tiro = st.slider("Tiro:", 0, 100, 70)
            with col_t3:
                pase = st.slider("Pase:", 0, 100, 70)
            with col_t4:
                regate = st.slider("Regate:", 0, 100, 70)
            with col_t5:
                defensa = st.slider("Defensa:", 0, 100, 50)
            with col_t6:
                fisico = st.slider("Físico:", 0, 100, 70)
            
            submit_button = st.form_submit_button(
                label="⚽ Predecir Valor de Mercado",
                type="primary"
            )
    
    if submit_button:
        # Preparar datos para predicción
        input_data = {
            "edad": edad,
            "valoracion_global": valoracion_global,
            "potencial": potencial,
            "pie_preferido": pie_preferido,
            "pie_debil": pie_debil,
            "habilidades_regate": habilidades_regate,
            "reputacion_internacional": reputacion,
            "anos_contrato_restantes": anos_contrato,
            "ritmo_velocidad": ritmo,
            "tiro_disparo": tiro,
            "pase": pase,
            "regate_gambeta": regate,
            "defensa": defensa,
            "fisico": fisico
        }
        
        try:
            response = sesion_http.post(API_URL_PREDECIR, json=input_data, timeout=30)
            response.raise_for_status()
            resultado = response.json()
            
            if "valor_predicho_eur" in resultado:
                valor_predicho = resultado["valor_predicho_eur"]
                confianza = resultado.get("confianza_prediccion", "N/A")
                percentil = resultado.get("percentil_valor", 0)
                
                with col_resultado:
                    st.subheader("Resultado de Predicción")
                    
                    st.markdown(f"""
                    <div class="ficha-jugador">
                        <div class="nombre-jugador">€{valor_predicho:,.0f}</div>
                        <div class="info-jugador">Valor de Mercado Predicho</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Confianza", confianza)
                    st.metric("Percentil", f"{percentil}%")
                    
                    st.success("Predicción realizada exitosamente")
                    
                    # Gráfico de comparación con percentiles
                    fig_perc = go.Figure()
                    
                    fig_perc.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=percentil,
                        title={'text': "Percentil de Valor"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': COLOR_DESTACADO},
                            'steps': [
                                {'range': [0, 25], 'color': COLOR_ACENTO_2},
                                {'range': [25, 50], 'color': COLOR_ACENTO_1},
                                {'range': [50, 75], 'color': COLOR_SECUNDARIO},
                                {'range': [75, 100], 'color': COLOR_DESTACADO}
                            ],
                        }
                    ))
                    
                    fig_perc.update_layout(
                        paper_bgcolor=COLOR_ACENTO_2,
                        font=dict(color=COLOR_SECUNDARIO),
                        height=300
                    )
                    
                    st.plotly_chart(fig_perc, use_container_width=True)
            else:
                with col_resultado:
                    st.error(f"Error en la predicción: {resultado.get('error', 'Formato desconocido')}")
        
        except requests.exceptions.RequestException as e:
            with col_resultado:
                st.error(f"Error de conexión con la API: {e}")

# FOOTER
st.markdown("---")
st.caption("© 2025 - Sistema de Scouting Inteligente FIFA | Powered by FastAPI + Streamlit + Random Forest ML")
