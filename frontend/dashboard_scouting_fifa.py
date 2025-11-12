import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
import os
import time
import base64
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from io import BytesIO
from PIL import Image

# DICCIONARIOS DE TRADUCCIÓN (INGLÉS → ESPAÑOL)
# Diccionario expandido con todas las posiciones y combinaciones posibles
TRADUCCIONES_POSICIONES = {
    # Portero
    "GK": "🥅 Portero (GK)",
    
    # Defensas
    "CB": "🛡️ Defensa Central (CB)",
    "LB": "⬅️ Lateral Izquierdo (LB)",
    "RB": "➡️ Lateral Derecho (RB)",
    "LWB": "⬅️ Carrilero Izquierdo (LWB)",
    "RWB": "➡️ Carrilero Derecho (RWB)",
    "SW": "🛡️ Líbero (SW)",
    
    # Mediocentros Defensivos
    "CDM": "🔒 Pivote Defensivo (CDM)",
    "DM": "🔒 Mediocentro Defensivo (DM)",
    
    # Mediocentros
    "CM": "⚙️ Centrocampista (CM)",
    "LCM": "⚙️ Centrocampista Izquierdo (LCM)",
    "RCM": "⚙️ Centrocampista Derecho (RCM)",
    
    # Mediocentros Ofensivos
    "CAM": "🎯 Mediapunta (CAM)",
    "AM": "🎯 Mediocentro Ofensivo (AM)",
    "LAM": "🎯 Mediapunta Izquierdo (LAM)",
    "RAM": "🎯 Mediapunta Derecho (RAM)",
    
    # Extremos/Interiores
    "LM": "⬅️ Interior Izquierdo (LM)",
    "RM": "➡️ Interior Derecho (RM)",
    "LW": "⬅️ Extremo Izquierdo (LW)",
    "RW": "➡️ Extremo Derecho (RW)",
    
    # Delanteros
    "CF": "⚡ Mediapunta Adelantado (CF)",
    "ST": "⚽ Delantero Centro (ST)",
    "LS": "⚽ Delantero Izquierdo (LS)",
    "RS": "⚽ Delantero Derecho (RS)",
    "LF": "⚽ Delantero Izquierdo (LF)",
    "RF": "⚽ Delantero Derecho (RF)"
}

TRADUCCIONES_NACIONALIDADES = {
    "Argentina": "Argentina",
    "Brazil": "Brasil",
    "Spain": "España",
    "France": "Francia",
    "Germany": "Alemania",
    "England": "Inglaterra",
    "Italy": "Italia",
    "Portugal": "Portugal",
    "Netherlands": "Países Bajos",
    "Belgium": "Bélgica",
    "Uruguay": "Uruguay",
    "Colombia": "Colombia",
    "Chile": "Chile",
    "Mexico": "México",
    "Croatia": "Croacia",
    "Poland": "Polonia",
    "Austria": "Austria",
    "Switzerland": "Suiza",
    "Sweden": "Suecia",
    "Denmark": "Dinamarca",
    "Norway": "Noruega",
    "United States": "Estados Unidos",
    "Canada": "Canadá",
    "Japan": "Japón",
    "Korea Republic": "Corea del Sur",
    "Australia": "Australia",
    "Serbia": "Serbia",
    "Turkey": "Turquía",
    "Russia": "Rusia",
    "Ukraine": "Ucrania",
    "Czech Republic": "República Checa",
    "Greece": "Grecia",
    "Romania": "Rumanía",
    "Scotland": "Escocia",
    "Wales": "Gales",
    "Ireland": "Irlanda",
    "Northern Ireland": "Irlanda del Norte",
    "Egypt": "Egipto",
    "Nigeria": "Nigeria",
    "Senegal": "Senegal",
    "Cameroon": "Camerún",
    "Ghana": "Ghana",
    "Ivory Coast": "Costa de Marfil",
    "Algeria": "Argelia",
    "Morocco": "Marruecos",
    "Tunisia": "Túnez",
    "South Africa": "Sudáfrica"
}

# DICCIONARIO SIMPLIFICADO DE POSICIONES (SIN EMOJI NI SIGLA ENTRE PARÉNTESIS)
TRADUCCIONES_POSICIONES_SIMPLE = {
    "GK": "Portero",
    "CB": "Defensa Central",
    "LB": "Lateral Izq.",
    "RB": "Lateral Der.",
    "LWB": "Carrilero Izq.",
    "RWB": "Carrilero Der.",
    "SW": "Líbero",
    "CDM": "Pivote",
    "DM": "Pivote",
    "CM": "Centrocampista",
    "LCM": "Centro Izq.",
    "RCM": "Centro Der.",
    "CAM": "Mediapunta",
    "AM": "Med. Ofensivo",
    "LAM": "Med. Izq.",
    "RAM": "Med. Der.",
    "LM": "Interior Izq.",
    "RM": "Interior Der.",
    "LW": "Extremo Izq.",
    "RW": "Extremo Der.",
    "CF": "Delantero",
    "ST": "Delantero",
    "LS": "Delantero Izq.",
    "RS": "Delantero Der.",
    "LF": "Delantero Izq.",
    "RF": "Delantero Der."
}

# FUNCIÓN AUXILIAR PARA TRADUCIR POSICIONES
def traducir_posicion(posicion_siglas):
    """
    Traduce las siglas de posición a texto descriptivo en español.
    
    - Posición única: Muestra formato completo con emoji (ej: "⚽ Delantero Centro (ST)")
    - Múltiples posiciones: Muestra versión simplificada (ej: "Delantero, Extremo Izq.")
    """
    if not posicion_siglas or posicion_siglas == 'N/A':
        return 'N/A'
    
    # Si hay múltiples posiciones separadas por coma
    if ',' in str(posicion_siglas):
        posiciones = [p.strip() for p in str(posicion_siglas).split(',')]
        # Para múltiples posiciones, usar traducción simple y limpia
        traducidas = [TRADUCCIONES_POSICIONES_SIMPLE.get(p, p) for p in posiciones]
        return ', '.join(traducidas)
    
    # Posición única - formato completo con emoji
    return TRADUCCIONES_POSICIONES.get(str(posicion_siglas).strip(), posicion_siglas)

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
    
    /* Botón compacto "Ficha" - responsive */
    .stButton > button[kind="primary"] {{
        padding: 4px 12px !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-radius: 8px !important;
        min-height: 28px !important;
        height: 28px !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
    }}
    
    /* Responsive: Reducir tamaño en pantallas medianas */
    @media (max-width: 1400px) {{
        .stButton > button[kind="primary"] {{
            font-size: 10px !important;
            padding: 4px 10px !important;
            letter-spacing: 0.3px !important;
        }}
    }}
    
    @media (max-width: 1200px) {{
        .stButton > button[kind="primary"] {{
            font-size: 9px !important;
            padding: 4px 8px !important;
            letter-spacing: 0.2px !important;
        }}
    }}
    
    @media (max-width: 992px) {{
        .stButton > button[kind="primary"] {{
            font-size: 8px !important;
            padding: 3px 6px !important;
            letter-spacing: 0.1px !important;
            min-height: 24px !important;
            height: 24px !important;
        }}
    }}
    
    @media (max-width: 768px) {{
        .stButton > button[kind="primary"] {{
            font-size: 7px !important;
            padding: 3px 5px !important;
            letter-spacing: 0px !important;
            min-height: 22px !important;
            height: 22px !important;
        }}
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

# ============================================================================
# SISTEMA DE CACHÉ DE IMÁGENES DE JUGADORES
# ============================================================================

# Directorio base para imágenes (fuera de Docker, persistente)
IMAGENES_DIR = "/app/datos/imagenes"
IMAGEN_GENERICA = "/app/datos/imagenes/jugador_generico.png"

def obtener_codigo_iso_pais(nacionalidad):
    """
    Obtiene el código ISO del país para la API de banderas
    
    Args:
        nacionalidad: Nombre del país
    
    Returns:
        str: Código ISO en minúsculas para flagcdn.com
    """
    # Mapeo de nombres de países a códigos ISO (casos especiales)
    pais_iso_map = {
        "England": "gb-eng", "Spain": "es", "Brazil": "br", "Argentina": "ar",
        "France": "fr", "Germany": "de", "Portugal": "pt", "Netherlands": "nl",
        "Belgium": "be", "Italy": "it", "Croatia": "hr", "Uruguay": "uy",
        "Colombia": "co", "Poland": "pl", "Egypt": "eg", "Senegal": "sn",
        "Korea Republic": "kr", "Japan": "jp", "Mexico": "mx", "Chile": "cl",
        "Ecuador": "ec", "Peru": "pe", "United States": "us", "Canada": "ca",
        "Scotland": "gb-sct", "Wales": "gb-wls", "Northern Ireland": "gb-nir",
        "Republic of Ireland": "ie", "Switzerland": "ch", "Austria": "at",
        "Czech Republic": "cz", "Denmark": "dk", "Sweden": "se", "Norway": "no",
        "Turkey": "tr", "Greece": "gr", "Serbia": "rs", "Bosnia Herzegovina": "ba",
        "Australia": "au", "New Zealand": "nz", "South Africa": "za", "Morocco": "ma",
        "Algeria": "dz", "Tunisia": "tn", "Nigeria": "ng", "Ghana": "gh",
        "Cameroon": "cm", "Ivory Coast": "ci", "Kenya": "ke", "China PR": "cn"
    }
    
    return pais_iso_map.get(nacionalidad, nacionalidad.lower()[:2] if nacionalidad else "xx")

def obtener_escudo_club(nombre_club):
    """
    Obtiene la URL del escudo del club de fútbol
    
    Args:
        nombre_club: Nombre del club
    
    Returns:
        str: URL del escudo o icono genérico
    """
    if not nombre_club or nombre_club in ['N/A', '', 'nan']:
        return "⚽"  # Emoji genérico
    
    # Mapeo manual de clubes principales (URLs verificadas desde ESPN - 100% funcionales)
    escudos_manuales = {
        # España - Top Teams
        "FC Barcelona": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/83.png&h=200&w=200",
        "Real Madrid": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/86.png&h=200&w=200",
        "Atletico Madrid": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/1068.png&h=200&w=200",
        "Atlético Madrid": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/1068.png&h=200&w=200",
        "Sevilla": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/92.png&h=200&w=200",
        "Valencia": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/94.png&h=200&w=200",
        "Villarreal": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/102.png&h=200&w=200",
        "Real Sociedad": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/89.png&h=200&w=200",
        "Real Betis": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/244.png&h=200&w=200",
        "Athletic Bilbao": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/244.png&h=200&w=200",
        
        # Inglaterra - Premier League
        "Manchester United": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/360.png&h=200&w=200",
        "Liverpool": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/364.png&h=200&w=200",
        "Chelsea": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/363.png&h=200&w=200",
        "Manchester City": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/382.png&h=200&w=200",
        "Arsenal": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/359.png&h=200&w=200",
        "Tottenham Hotspur": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/367.png&h=200&w=200",
        "Leicester City": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/375.png&h=200&w=200",
        "West Ham United": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/371.png&h=200&w=200",
        "Everton": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/368.png&h=200&w=200",
        "Aston Villa": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/362.png&h=200&w=200",
        "Newcastle United": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/361.png&h=200&w=200",
        "Brighton": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/331.png&h=200&w=200",
        "Brentford": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/337.png&h=200&w=200",
        "Fulham": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/370.png&h=200&w=200",
        "Wolves": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/380.png&h=200&w=200",
        "Crystal Palace": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/384.png&h=200&w=200",
        "Southampton": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/376.png&h=200&w=200",
        "Leeds United": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/357.png&h=200&w=200",
        
        # Italia - Serie A
        "Juventus": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/111.png&h=200&w=200",
        "Inter": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/102.png&h=200&w=200",
        "AC Milan": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/103.png&h=200&w=200",
        "Napoli": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/114.png&h=200&w=200",
        "Roma": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/104.png&h=200&w=200",
        "Lazio": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/110.png&h=200&w=200",
        "Atalanta": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/102.png&h=200&w=200",
        "Fiorentina": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/100.png&h=200&w=200",
        "Torino": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/109.png&h=200&w=200",
        "Sampdoria": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/108.png&h=200&w=200",
        "Udinese": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/112.png&h=200&w=200",
        
        # Alemania - Bundesliga
        "Bayern Munich": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/132.png&h=200&w=200",
        "FC Bayern München": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/132.png&h=200&w=200",
        "Borussia Dortmund": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/124.png&h=200&w=200",
        "RB Leipzig": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/11420.png&h=200&w=200",
        "Bayer Leverkusen": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/131.png&h=200&w=200",
        "Wolfsburg": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/171.png&h=200&w=200",
        "Eintracht Frankfurt": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/125.png&h=200&w=200",
        "Borussia Monchengladbach": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/135.png&h=200&w=200",
        "Stuttgart": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/134.png&h=200&w=200",
        "Schalke 04": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/130.png&h=200&w=200",
        
        # Francia - Ligue 1
        "Paris Saint Germain": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/160.png&h=200&w=200",
        "Paris Saint-Germain": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/160.png&h=200&w=200",
        "Lyon": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/167.png&h=200&w=200",
        "Marseille": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/176.png&h=200&w=200",
        "Monaco": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/174.png&h=200&w=200",
        "Lille": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/166.png&h=200&w=200",
        "Rennes": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/169.png&h=200&w=200",
        
        # Portugal
        "FC Porto": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/182.png&h=200&w=200",
        
        # Holanda - Eredivisie
        "Ajax": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/139.png&h=200&w=200",
        "PSV": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/147.png&h=200&w=200",
        "Feyenoord": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/140.png&h=200&w=200",
        
        # Escocia
        "Celtic": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/273.png&h=200&w=200",
        "Rangers": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/274.png&h=200&w=200",
        
        # Bélgica
        "Club Brugge": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/304.png&h=200&w=200",
        "Anderlecht": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/232.png&h=200&w=200",
        
        # Turquía
        "Fenerbahce": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/606.png&h=200&w=200",
    }
    
    # Buscar coincidencia exacta
    if nombre_club in escudos_manuales:
        return escudos_manuales[nombre_club]
    
    # Buscar coincidencia parcial (ej: "FC Barcelona" contiene "Barcelona")
    for club, url in escudos_manuales.items():
        if club.lower() in nombre_club.lower() or nombre_club.lower() in club.lower():
            return url
    
    # Si no se encuentra, devolver emoji
    return "⚽"

def obtener_escudo_liga(nombre_liga):
    """
    Obtiene la URL del escudo de la liga de fútbol.
    Retorna la URL del escudo o un emoji si no se encuentra.
    """
    if not nombre_liga or nombre_liga in ['N/A', '', 'nan']:
        return "🏆"
    
    # Diccionario de escudos de las principales ligas (URLs verificadas desde ESPN - 100% funcionales)
    escudos_ligas = {
        # Top 5 Ligas Europeas
        "Spain Primera Division": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/15.png&h=200&w=200",
        "La Liga": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/15.png&h=200&w=200",
        "English Premier League": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/23.png&h=200&w=200",
        "Premier League": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/23.png&h=200&w=200",
        "Italian Serie A": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/12.png&h=200&w=200",
        "Serie A": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/12.png&h=200&w=200",
        "German 1. Bundesliga": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/10.png&h=200&w=200",
        "Bundesliga": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/10.png&h=200&w=200",
        "French Ligue 1": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/9.png&h=200&w=200",
        "Ligue 1": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/9.png&h=200&w=200",
        
        # Otras Ligas Europeas
        "Portuguese Liga ZON SAGRES": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/14.png&h=200&w=200",
        "Liga Portugal": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/14.png&h=200&w=200",
        "Dutch Eredivisie": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/11.png&h=200&w=200",
        "Eredivisie": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/11.png&h=200&w=200",
        "Scottish Premiership": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/40.png&h=200&w=200",
        "Belgian First Division A": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/22.png&h=200&w=200",
        "Turkish Super Lig": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/17.png&h=200&w=200",
        
        # Competiciones Europeas
        "UEFA Champions League": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/2.png&h=200&w=200",
        "UEFA Europa League": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/2310.png&h=200&w=200",
        
        # América
        "Major League Soccer": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/19.png&h=200&w=200",
        "MLS": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/19.png&h=200&w=200",
        "Liga MX": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/22.png&h=200&w=200",
        "Copa Sudamericana": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/2344.png&h=200&w=200",
        
        # Segunda División
        "English League Championship": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/24.png&h=200&w=200",
        "Championship": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/24.png&h=200&w=200",
        
        # Ligas Europeas Adicionales
        "Swiss Super League": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/16.png&h=200&w=200",
        "Norwegian Eliteserien": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/41.png&h=200&w=200",
        "Swedish Allsvenskan": "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/42.png&h=200&w=200",
    }
    
    # Búsqueda exacta
    if nombre_liga in escudos_ligas:
        return escudos_ligas[nombre_liga]
    
    # Búsqueda parcial (case insensitive)
    for liga, url in escudos_ligas.items():
        if liga.lower() in nombre_liga.lower() or nombre_liga.lower() in liga.lower():
            return url
    
    # Si no se encuentra, retornar emoji
    return "🏆"

def descargar_imagen_generica():
    """Descarga una imagen genérica de jugador si no existe"""
    if os.path.exists(IMAGEN_GENERICA):
        return
    
    try:
        # URL de imagen genérica de futbolista (silueta profesional)
        url_generica = "https://cdn.pixabay.com/photo/2016/11/14/17/39/person-1824144_960_720.png"
        
        response = requests.get(url_generica, timeout=5)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(IMAGEN_GENERICA), exist_ok=True)
            with open(IMAGEN_GENERICA, 'wb') as f:
                f.write(response.content)
            print("✅ Imagen genérica descargada")
        else:
            print(f"⚠️  No se pudo descargar imagen genérica (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error descargando imagen genérica: {e}")

def generar_url_foto_sofifa(id_sofifa, año_fifa):
    """
    Genera la URL de la foto del jugador desde el CDN de SoFIFA
    
    Patrón descubierto:
    https://cdn.sofifa.net/players/{AAA}/{BBB}/{YY}_240.png
    
    Donde:
    - AAA = primeros 3 dígitos del id_sofifa (con padding de ceros)
    - BBB = últimos 3 dígitos del id_sofifa (con padding de ceros)
    - YY = últimos 2 dígitos del año (21 para 2021, 20 para 2020, etc.)
    
    Ejemplos:
    - Messi (158023) FIFA 21: https://cdn.sofifa.net/players/158/023/21_240.png
    - Ronaldo (20801) FIFA 21: https://cdn.sofifa.net/players/020/801/21_240.png
    """
    try:
        # Convertir id a string y rellenar con ceros a la izquierda (6 dígitos)
        id_str = str(int(id_sofifa)).zfill(6)
        
        # Extraer primeros 3 y últimos 3 dígitos
        primeros_3 = id_str[:3]
        ultimos_3 = id_str[-3:]
        
        # Extraer últimos 2 dígitos del año
        año_2_digitos = str(int(año_fifa))[-2:]
        
        # Construir URL
        url = f"https://cdn.sofifa.net/players/{primeros_3}/{ultimos_3}/{año_2_digitos}_240.png"
        
        return url, primeros_3, ultimos_3, año_2_digitos
    except Exception as e:
        print(f"❌ Error generando URL foto - ID: {id_sofifa}, Año: {año_fifa}, Error: {e}")
        return None, None, None, None

def obtener_foto_jugador(id_sofifa, año_fifa):
    """
    Obtiene la foto del jugador desde caché local o la descarga si no existe.
    Utiliza estructura jerárquica: imagenes/{AAA}/{BBB}/{YY}_240.png
    
    Returns:
        PIL.Image: Imagen del jugador o imagen genérica si no existe
    """
    try:
        # Generar URL y estructura de carpetas
        url, primeros_3, ultimos_3, año_2_digitos = generar_url_foto_sofifa(id_sofifa, año_fifa)
        
        if not url:
            # Si falla generar URL, usar imagen genérica
            if os.path.exists(IMAGEN_GENERICA):
                return Image.open(IMAGEN_GENERICA)
            return None
        
        # Ruta local con estructura jerárquica: imagenes/AAA/BBB/YY_240.png
        ruta_local = os.path.join(IMAGENES_DIR, primeros_3, ultimos_3, f"{año_2_digitos}_240.png")
        
        # Si existe en caché, cargarla
        if os.path.exists(ruta_local):
            print(f"📁 Cargando desde caché: {ruta_local}")
            return Image.open(ruta_local)
        
        # Si no existe, descargar desde SoFIFA
        print(f"⬇️  Descargando: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
            
            # Guardar imagen en caché
            with open(ruta_local, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Imagen guardada en: {ruta_local}")
            
            # Cargar y retornar imagen
            return Image.open(BytesIO(response.content))
        else:
            # Foto no existe en SoFIFA, usar genérica
            print(f"⚠️  Foto no disponible (Status: {response.status_code}), usando genérica")
            if os.path.exists(IMAGEN_GENERICA):
                return Image.open(IMAGEN_GENERICA)
            return None
            
    except Exception as e:
        print(f"❌ Error obteniendo foto: {e}")
        # En caso de error, intentar usar imagen genérica
        if os.path.exists(IMAGEN_GENERICA):
            return Image.open(IMAGEN_GENERICA)
        return None

# Descargar imagen genérica al iniciar la app
descargar_imagen_generica()

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

def obtener_perfil_jugador(jugador_id, año=None):
    """Obtiene el perfil completo de un jugador"""
    try:
        url = API_URL_PERFIL.format(id=jugador_id)
        params = {"año": año} if año else {}
        response = sesion_http.get(url, params=params, timeout=10)
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

def mostrar_ficha_jugador(jugador_id, jugador_nombre):
    """Muestra la ficha detallada de un jugador con gráfico radar"""
    
    perfil = obtener_perfil_jugador(jugador_id)
    
    if perfil and "jugador" in perfil:
        jugador = perfil["jugador"]
        prediccion = perfil.get("prediccion_ml", {})
        
        # Obtener escudo del club para top jugadores
        club_top = jugador.get('club', 'Sin club')
        escudo_club_top = obtener_escudo_club(club_top)
        club_icon = f'<img src="{escudo_club_top}" style="width: 18px; height: 18px; vertical-align: middle; object-fit: contain;" onerror="this.style.display=\'none\'">' if escudo_club_top != "⚽" else "⚽"
        
        st.markdown(f"""
        <div class="ficha-jugador">
            <div class="nombre-jugador">{jugador.get('nombre_corto', 'N/A')}</div>
            <div class="info-jugador">
                {club_icon} {club_top} | {jugador.get('nacionalidad', 'N/A')} | {jugador.get('edad', 'N/A')} años
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            # Foto del jugador (desde caché local o descarga)
            id_sofifa = jugador.get("id_sofifa")
            año_datos = jugador.get("año_datos", 2021)
            
            if id_sofifa and año_datos:
                img = obtener_foto_jugador(id_sofifa, año_datos)
                if img:
                    st.image(img, width=200)
                else:
                    st.info("Sin foto disponible")
            else:
                st.info("Sin foto disponible")
            
            # Información básica
            st.markdown("##### Información")
            st.write(f"**Posición:** {traducir_posicion(jugador.get('posiciones_jugador', 'N/A'))}")
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
            
            # Clasificación (con tolerancia por defecto de 8%)
            tolerancia_default = 8
            if diferencia > tolerancia_default:
                st.success(f"✓ {clasificacion} (+{diferencia:.1f}%)")
                st.info("Jugador potencialmente INFRAVALORADO")
            elif diferencia < -tolerancia_default:
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
    
    # Header del modal con selector de año y tolerancia
    col_header_1, col_header_2, col_header_3 = st.columns([2.5, 1, 1.5])
    
    with col_header_1:
        st.markdown(f"### {jugador_nombre}")
    
    with col_header_2:
        # Obtener años disponibles para este jugador
        try:
            url_años = f"{API_BASE_URL}/jugadores/{jugador_id}/años"
            response = sesion_http.get(url_años, timeout=5)
            if response.status_code == 200:
                años_disponibles = response.json().get("años", [año_fifa])
            else:
                años_disponibles = [año_fifa]
        except:
            años_disponibles = [año_fifa]
        
        # Selector de año con callback para cerrar y reabrir modal
        año_seleccionado = st.selectbox(
            "📅 Año FIFA",
            options=sorted(años_disponibles, reverse=True),
            index=sorted(años_disponibles, reverse=True).index(año_fifa) if año_fifa in años_disponibles else 0,
            key=f"selector_año_{jugador_id}_{año_fifa}"
        )
        
        # Si cambió el año, cerrar modal y actualizar session_state para reabrirlo
        if año_seleccionado != año_fifa:
            st.session_state.modal_jugador_id = jugador_id
            st.session_state.modal_jugador_nombre = jugador_nombre
            st.session_state.modal_jugador_año = año_seleccionado
            st.session_state.mostrar_modal = True
            st.session_state.modal_clic_reciente = True
            st.rerun()
    
    with col_header_3:
        # Slider de tolerancia para clasificación
        tolerancia_porcentaje = st.slider(
            "🎯 Tolerancia (%)",
            min_value=1,
            max_value=30,
            value=8,
            step=1,
            key=f"tolerancia_{jugador_id}_{año_fifa}",
            help="Porcentaje de diferencia para considerar infravalorado/sobrevalorado"
        )
    
    st.markdown("---")
    
    # Cargar perfil del jugador con el año seleccionado
    perfil = obtener_perfil_jugador(jugador_id, año_fifa)
    
    if perfil and "jugador" in perfil:
        jugador = perfil["jugador"]
        prediccion = perfil.get("prediccion_ml", {})
        
        # SECCIÓN 1: INFO BÁSICA + FOTO
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Foto del jugador (desde caché local o descarga)
            id_sofifa = jugador.get("id_sofifa")
            
            if id_sofifa and año_fifa:
                img = obtener_foto_jugador(id_sofifa, año_fifa)
                if img:
                    st.image(img, width=250)
                else:
                    st.info("📷 Sin foto disponible")
            else:
                st.info("📷 Sin foto disponible")
            
            # Info básica en tarjetas
            nacionalidad_modal = jugador.get('nacionalidad', 'N/A')
            pais_iso_modal = obtener_codigo_iso_pais(nacionalidad_modal)
            bandera_url_modal = f"https://flagcdn.com/32x24/{pais_iso_modal}.png"
            
            # Obtener escudo del club para el modal
            club_modal = jugador.get('club', 'N/A')
            escudo_club_modal = obtener_escudo_club(club_modal)
            club_html = f'<img src="{escudo_club_modal}" style="width: 24px; height: 24px; vertical-align: middle; margin-right: 5px; object-fit: contain;" onerror="this.style.display=\'none\'">' if escudo_club_modal != "⚽" else "🏟️"
            
            # Obtener escudo de la liga para el modal
            liga_modal = jugador.get('liga', 'N/A')
            escudo_liga_modal = obtener_escudo_liga(liga_modal)
            liga_html = f'<img src="{escudo_liga_modal}" style="width: 24px; height: 24px; vertical-align: middle; margin-right: 5px; object-fit: contain;" onerror="this.style.display=\'none\'">' if escudo_liga_modal != "🏆" else "🏆"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%); 
                 padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {COLOR_ACENTO_1};'>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>{club_html} Club:</b> {club_modal}</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'><b>{liga_html} Liga:</b> {liga_modal}</p>
                <p style='margin: 5px 0; color: {COLOR_SECUNDARIO};'>
                    <b><img src="{bandera_url_modal}" style="width: 24px; height: 18px; vertical-align: middle; margin-right: 5px;" onerror="this.style.display='none'"> Nacionalidad:</b> {nacionalidad_modal}
                </p>
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
                st.metric("📍 Posición", traducir_posicion(jugador.get('posiciones_jugador', 'N/A')))
        
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
                
                # RECALCULAR clasificación dinámicamente basada en tolerancia del slider
                if diferencia > tolerancia_porcentaje:
                    clasificacion = "INFRAVALORADO"
                elif diferencia < -tolerancia_porcentaje:
                    clasificacion = "SOBREVALORADO"
                else:
                    clasificacion = "JUSTO"
                
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
                
                # Clasificación con badge (usando tolerancia variable del slider)
                if diferencia > tolerancia_porcentaje:
                    st.success(f"✅ **{clasificacion}** (+{diferencia:.1f}%)")
                    st.info("🔍 **Oportunidad:** Jugador potencialmente INFRAVALORADO")
                elif diferencia < -tolerancia_porcentaje:
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
                
                # Botón para cerrar modal
                st.markdown("---")
                if st.button("❌ Cerrar", use_container_width=True, type="secondary"):
                    st.session_state.mostrar_modal = False
                    st.rerun()
    
    else:
        st.error("❌ No se pudo cargar la información del jugador")
        st.info("Intenta refrescar la página o selecciona otro jugador")
        
        # Botón para cerrar modal en caso de error
        if st.button("❌ Cerrar", use_container_width=True, type="secondary"):
            st.session_state.mostrar_modal = False
            st.rerun()

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
    <div style='margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
        <p style='color: rgba(255,255,255,0.85); font-size: 15px; margin: 8px 0; font-weight: 600;'>
            Universidad Regional Autónoma de los Andes (UNIANDES)
        </p>
        <p style='color: rgba(255,255,255,0.75); font-size: 13px; margin: 5px 0;'>
            Ingeniería de Software | Analítica con Python | Proyecto Final de Graduación
        </p>
        <p style='color: rgba(255,255,255,0.7); font-size: 13px; margin: 5px 0;'>
            Prof. Juan Felipe Nájera | Noviembre 2025
        </p>
    </div>
    <div style='margin-top: 15px; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 15px; backdrop-filter: blur(5px);'>
        <p style='color: rgba(255,255,255,0.8); font-size: 13px; margin: 5px 0; font-weight: 500;'>
            👥 Grupo 7
        </p>
        <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 10px;'>
            <span style='color: rgba(255,255,255,0.75); font-size: 12px;'>Alberto Alexander Aldás Villacrés</span>
            <span style='color: rgba(255,255,255,0.75); font-size: 12px;'>Cristian Joel Riofrío Medina</span>
            <span style='color: rgba(255,255,255,0.75); font-size: 12px;'>Wilson Fernando Saavedra Álvarez</span>
        </div>
    </div>
    <div style='margin-top: 20px; padding: 15px; background: rgba(74, 222, 128, 0.15); border-radius: 15px; border: 2px solid rgba(74, 222, 128, 0.3);'>
        <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 5px 0; font-weight: 600;'>
            🌐 Enlaces del Proyecto
        </p>
        <div style='display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; margin-top: 12px;'>
            <a href='https://grupo7fifa.uniandes.site/' target='_blank' style='color: #4ade80; font-size: 12px; text-decoration: none; font-weight: 600; transition: opacity 0.3s;' onmouseover='this.style.opacity="0.7"' onmouseout='this.style.opacity="1"'>
                🚀 Sistema en Producción
            </a>
            <span style='color: rgba(255,255,255,0.5);'>|</span>
            <a href='https://github.com/btoaldas/seminario-complexivo-grupo-7' target='_blank' style='color: #4ade80; font-size: 12px; text-decoration: none; font-weight: 600; transition: opacity 0.3s;' onmouseover='this.style.opacity="0.7"' onmouseout='this.style.opacity="1"'>
                📁 Repositorio GitHub
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# RESETEAR MODAL AL INICIO (se activará solo con clic explícito en "Ficha")
# Si no hay flag de "acabo de hacer clic", cerrar modal
if 'modal_clic_reciente' not in st.session_state:
    st.session_state.modal_clic_reciente = False

if not st.session_state.modal_clic_reciente:
    st.session_state.mostrar_modal = False
else:
    # Resetear el flag para la próxima ejecución
    st.session_state.modal_clic_reciente = False

# MODAL DE PRESENTACIÓN DE DEFENSA (HTML PURO - 100% PANTALLA SIN STREAMLIT)
if 'mostrar_presentacion' not in st.session_state:
    st.session_state.mostrar_presentacion = False

if st.session_state.mostrar_presentacion:
    # Cargar HTML desde archivo
    ruta_presentacion = os.path.join(os.path.dirname(__file__), "presentacion_defensa.html")
    
    try:
        with open(ruta_presentacion, "r", encoding="utf-8") as f:
            presentacion_html = f.read()
        
        # Inyectar botón de cierre minimalista + script de comunicación con Streamlit
        boton_cierre = """
        <button id="btn-cerrar-presentacion" style="
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 10000;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            border: 1px solid rgba(0,0,0,0.1);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 24px;
            font-weight: normal;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transition: all 0.2s;
            line-height: 1;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        "
        onmouseover="this.style.background='rgba(255, 255, 255, 1)'; this.style.transform='scale(1.05)';"
        onmouseout="this.style.background='rgba(255, 255, 255, 0.95)'; this.style.transform='scale(1)';"
        onclick="cerrarModal()">
            ✕
        </button>
        <script>
            function cerrarModal() {
                // Enviar señal a Streamlit para cerrar modal
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    key: 'cerrar_modal_signal',
                    value: true
                }, '*');
                
                // Forzar recarga de la página padre después de 100ms
                setTimeout(function() {
                    try {
                        // Acceder al location del padre
                        const parentUrl = window.parent.location;
                        const currentUrl = parentUrl.href;
                        const baseUrl = currentUrl.split('?')[0];
                        window.parent.location.href = baseUrl;
                    } catch (e) {
                        console.error('Error al cerrar:', e);
                        // Fallback: intentar recargar desde el iframe
                        window.top.location.reload();
                    }
                }, 100);
            }
            
            // Enviar mensaje de carga completa
            window.addEventListener('load', function() {
                console.log('Presentación cargada completamente');
            });
        </script>
        </body>
        """
        
        presentacion_modificada = presentacion_html.replace("</body>", boton_cierre)
        
        # Renderizar la presentación completa sin iframe de Streamlit
        st.markdown(f"""
        <style>
            /* Ocultar TODOS los elementos de Streamlit incluyendo SIDEBAR */
            header, footer, .stApp > header, [data-testid="stHeader"], 
            [data-testid="stToolbar"], .stDeployButton, 
            [data-testid="stDecoration"], [data-testid="stStatusWidget"],
            #MainMenu, .stActionButton, [data-testid="stSidebar"],
            [data-testid="collapsedControl"] {{
                display: none !important;
                visibility: hidden !important;
                width: 0 !important;
                min-width: 0 !important;
            }}
            
            /* Hacer que el contenedor principal ocupe 100% */
            .main, .block-container, section[data-testid="stMain"] {{
                padding: 0 !important;
                max-width: 100% !important;
                margin: 0 !important;
                margin-left: 0 !important;
            }}
            
            /* Eliminar padding del iframe */
            iframe {{
                border: none !important;
                width: 100vw !important;
                height: 100vh !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
            }}
        </style>
        <script>
            // Cerrar sidebar automáticamente al cargar modal
            window.parent.document.querySelector('[data-testid="collapsedControl"]')?.click();
        </script>
        """, unsafe_allow_html=True)
        
        # Renderizar HTML completo ocupando toda la pantalla
        # El script en el HTML se encarga de cerrar recargando la página padre
        components.html(presentacion_modificada, height=900, scrolling=True)
        
        # Este código no se ejecutará porque el script recarga la página
        # pero está como fallback de seguridad
        
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo de presentación.")
        if st.button("🔄 Recargar"):
            st.session_state.mostrar_presentacion = False
            st.rerun()

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
    
    # CSS GLOBAL: LIGHT MODE = DARK MODE (COLORES IDÉNTICOS)
    st.markdown("""
    <style>
        /* ============================================ */
        /* HEADER NATIVO DE STREAMLIT - INVERTIR      */
        /* ============================================ */
        [data-testid="stHeader"] {
            background-color: #0e1117 !important;
        }
        
        [data-testid="stHeader"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stToolbar"] {
            background-color: #0e1117 !important;
        }
        
        [data-testid="stToolbar"] * {
            color: #ffffff !important;
        }
        
        /* ============================================ */
        /* INPUTS - Fondo oscuro con texto blanco     */
        /* ============================================ */
        
        /* Textbox / Input fields */
        .main input[type="text"],
        .main input[type="number"],
        .main textarea,
        [data-testid="stSidebar"] input[type="text"],
        [data-testid="stSidebar"] input[type="number"],
        [data-testid="stSidebar"] textarea {
            background-color: #262730 !important;
            color: #ffffff !important;
            border: 1px solid #444654 !important;
        }
        
        /* Number Input - Botones de incremento/decremento */
        [data-testid="stNumberInput"] {
            background-color: #262730 !important;
        }
        
        [data-testid="stNumberInput"] input {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        [data-testid="stNumberInput"] button {
            background-color: #262730 !important;
            color: #ffffff !important;
            border-color: #444654 !important;
        }
        
        [data-testid="stNumberInput"] button:hover {
            background-color: #667eea !important;
            color: #ffffff !important;
        }
        
        [data-testid="stNumberInput"] div[data-baseweb="input"] {
            background-color: #262730 !important;
        }
        
        /* Botones de step (+ y -) */
        [data-testid="stNumberInput"] [data-baseweb="button-group"] button {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        /* Selectbox / Dropdown - TODOS */
        .main [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-baseweb="select"],
        [data-baseweb="select"] > div,
        div[data-baseweb="select"] {
            background-color: #262730 !important;
            color: #ffffff !important;
            border: 1px solid #444654 !important;
        }
        
        /* Input dentro del select */
        [data-baseweb="select"] input {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        /* Valor seleccionado */
        [data-baseweb="select"] [role="button"] {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        /* Texto del placeholder y valor */
        [data-baseweb="select"] span,
        [data-baseweb="select"] div {
            color: #ffffff !important;
        }
        
        /* Multiselect */
        .main [data-baseweb="tag"],
        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background-color: #667eea !important;
            color: #ffffff !important;
        }
        
        /* Dropdown options */
        [data-baseweb="menu"],
        [data-baseweb="popover"] {
            background-color: #262730 !important;
        }
        
        [data-baseweb="menu"] li,
        [data-baseweb="menu"] div {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background-color: #667eea !important;
        }
        
        /* Lista desplegable del selector */
        [data-baseweb="popover"] [data-baseweb="menu"] {
            background-color: #262730 !important;
        }
        
        /* Opciones individuales en lista */
        [data-baseweb="menu"] [role="option"] {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        [data-baseweb="menu"] [role="option"]:hover {
            background-color: #667eea !important;
        }
        
        /* Contenedor de opciones */
        [data-baseweb="menu"] ul {
            background-color: #262730 !important;
        }
        
        /* Panel de opciones (popover) */
        [role="listbox"],
        [role="listbox"] ul,
        [role="listbox"] li {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        /* Opciones en el listbox */
        [role="option"] {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {
            background-color: #667eea !important;
            color: #ffffff !important;
        }
        
        /* Overlay del popover */
        [data-baseweb="popover"] {
            background-color: transparent !important;
        }
        
        [data-baseweb="popover"] > div {
            background-color: #262730 !important;
        }
        
        /* Slider */
        .main [data-testid="stSlider"] div[role="slider"],
        [data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
            background-color: #667eea !important;
        }
        
        /* ============================================ */
        /* MODALES/DIALOG - Fondo oscuro completo     */
        /* ============================================ */
        
        /* Fondo del modal */
        [data-testid="stDialog"],
        [data-testid="stModal"] {
            background-color: #0e1117 !important;
        }
        
        /* Contenido del modal */
        [data-testid="stDialog"] [data-testid="stVerticalBlock"],
        [data-testid="stModal"] [data-testid="stVerticalBlock"] {
            background-color: #0e1117 !important;
        }
        
        /* Header del modal */
        [data-testid="stDialog"] [data-testid="stMarkdown"],
        [data-testid="stModal"] [data-testid="stMarkdown"] {
            background-color: #0e1117 !important;
        }
        
        /* Texto en modal */
        [data-testid="stDialog"] *,
        [data-testid="stModal"] * {
            color: #ffffff !important;
        }
        
        /* Selectores dentro del modal */
        [data-testid="stDialog"] [data-baseweb="select"] > div,
        [data-testid="stModal"] [data-baseweb="select"] > div {
            background-color: #262730 !important;
            color: #ffffff !important;
        }
        
        /* Contenedor principal del modal */
        [role="dialog"] {
            background-color: #0e1117 !important;
        }
        
        [role="dialog"] [data-testid="stVerticalBlock"] {
            background-color: #0e1117 !important;
        }
        
        /* Métricas en modal */
        [data-testid="stDialog"] [data-testid="stMetric"],
        [data-testid="stModal"] [data-testid="stMetric"] {
            background-color: #262730 !important;
        }
        
        /* Gráficos en modal */
        [data-testid="stDialog"] [data-testid="stPlotlyChart"],
        [data-testid="stModal"] [data-testid="stPlotlyChart"] {
            background-color: #0e1117 !important;
        }
        
        /* ============================================ */
        /* SIDEBAR - Colores para light y dark mode   */
        /* ============================================ */
        [data-testid="stSidebar"] h2 {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] div h2 {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #fafafa !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label,
        [data-testid="stSidebar"] [data-testid="stMultiSelect"] label,
        [data-testid="stSidebar"] [data-testid="stTextInput"] label {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {
            color: #b0b0b0 !important;
            opacity: 0.8 !important;
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #f0f0f0 !important;
        }
        
        [data-testid="stSidebar"] .stHelp {
            color: #d0d0d0 !important;
        }
        
        /* ============================================ */
        /* CONTENIDO PRINCIPAL - TODO IGUAL QUE DARK   */
        /* ============================================ */
        
        /* Headers de tablas (th) - FORZAR BLANCO */
        .main table thead th {
            color: #ffffff !important;
            background-color: #667eea !important;
            font-weight: 600 !important;
        }
        
        /* Celdas de tablas (td) - FORZAR BLANCO */
        .main table tbody td {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Números en celdas (año FIFA, edad, etc) - FORZAR BLANCO */
        .main table tbody td strong,
        .main table tbody td b {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Headers de columnas personalizados (st.markdown con **) - FORZAR BLANCO */
        .main [data-testid="column"] strong,
        .main [data-testid="column"] b,
        .main [data-testid="column"] em {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        /* Contenido de columnas (valores de celdas) - FORZAR BLANCO */
        .main [data-testid="column"] div,
        .main [data-testid="column"] p,
        .main [data-testid="column"] span {
            color: #ffffff !important;
        }
        
        /* Números y texto en divs dentro de columnas - FORZAR BLANCO */
        .main [data-testid="column"] div[style*="text-align"] {
            color: #ffffff !important;
        }
        
        /* TODO EL TEXTO EN BLOQUES VERTICALES - FORZAR BLANCO */
        .main [data-testid="stVerticalBlock"] *,
        .main [data-testid="stVerticalBlock"] div,
        .main [data-testid="stVerticalBlock"] p,
        .main [data-testid="stVerticalBlock"] span,
        .main [data-testid="stVerticalBlock"] strong,
        .main [data-testid="stVerticalBlock"] b {
            color: #ffffff !important;
        }
        
        /* Texto de paginación (Página 1 de X) - FORZAR BLANCO */
        .main p {
            color: #ffffff !important;
        }
        
        /* Headers de cualquier tipo - FORZAR BLANCO */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: #ffffff !important;
        }
        
        /* Todo texto en markdown - FORZAR BLANCO */
        .main [data-testid="stMarkdown"] *,
        .main [data-testid="stMarkdown"] p,
        .main [data-testid="stMarkdown"] div,
        .main [data-testid="stMarkdown"] span {
            color: #ffffff !important;
        }
        
        /* Bloques horizontales - FORZAR BLANCO */
        .main [data-testid="stHorizontalBlock"] *,
        .main [data-testid="stHorizontalBlock"] p,
        .main [data-testid="stHorizontalBlock"] div {
            color: #ffffff !important;
        }
        
        /* REGLA GLOBAL: TODO EL TEXTO EN .main DEBE SER BLANCO */
        .main * {
            color: #ffffff !important;
        }
        
        /* Forzar blanco en elementos específicos de Streamlit */
        .element-container * {
            color: #ffffff !important;
        }
        
        .stMarkdown * {
            color: #ffffff !important;
        }
        
        /* Forzar headers de tabla custom */
        .main .element-container strong,
        .main .element-container b {
            color: #ffffff !important;
        }
        
        /* Títulos H3, H4, H5 en contenido principal */
        .main h3,
        .main h4,
        .main h5 {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Forzar texto en containers de Streamlit */
        div[data-testid="element-container"] *,
        div[data-testid="element-container"] p,
        div[data-testid="element-container"] span,
        div[data-testid="element-container"] strong {
            color: #ffffff !important;
        }
        
        /* Spans y divs con texto */
        .main span,
        .main div {
            color: #fafafa !important;
        }
        
        /* Labels en contenido principal */
        .main label {
            color: #fafafa !important;
            font-weight: 500 !important;
        }
        
        /* Texto en expanders */
        .main [data-testid="stExpander"] {
            color: #fafafa !important;
        }
        
        .main [data-testid="stExpander"] p,
        .main [data-testid="stExpander"] span,
        .main [data-testid="stExpander"] div {
            color: #fafafa !important;
        }
        
        /* Nombres de clubes y ligas */
        .main strong,
        .main b {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        /* Métricas (números grandes) */
        .main [data-testid="stMetric"] {
            color: #ffffff !important;
        }
        
        .main [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        .main [data-testid="stMetricLabel"] {
            color: #fafafa !important;
        }
        
        /* Cards y contenedores */
        .main [data-testid="stVerticalBlock"] p,
        .main [data-testid="stVerticalBlock"] span {
            color: #fafafa !important;
        }
        
        /* Markdown renderizado */
        .main .stMarkdown {
            color: #fafafa !important;
        }
        
        .main .stMarkdown p,
        .main .stMarkdown span,
        .main .stMarkdown div {
            color: #fafafa !important;
        }
        
        /* Listas (Jugadores Infravalorados/Sobrevalorados) */
        .main ul li,
        .main ol li {
            color: #fafafa !important;
        }
        
        /* Encabezados en listas */
        .main ul li strong,
        .main ol li strong {
            color: #ffffff !important;
        }
        
        /* Texto de información básica (Edad:, Valoración Global:) */
        .main div[data-testid="column"] p,
        .main div[data-testid="column"] span {
            color: #fafafa !important;
        }
        
        /* Números de atributos (Ritmo: 100, Tiro: 100) */
        .main div[data-testid="column"] strong {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
        
   
    
    # FILTROS EN SIDEBAR MEJORADO
    with st.sidebar:
        # BOTÓN DE PRESENTACIÓN DE DEFENSA
        if st.button("📄 ONE PAGE", use_container_width=True, type="primary", key="btn_presentacion"):
            st.session_state.mostrar_presentacion = True
            st.rerun()  # Forzar recarga inmediata
        
        
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
        
        # ⚽ FILTRO POR NOMBRE (NUEVO)
        st.markdown("### 🔍 Buscar por Nombre")
        nombre_busqueda = st.text_input(
            "Nombre del jugador:",
            placeholder="Ej: Messi, Neymar, Ronaldo...",
            help="Búsqueda flexible: funciona con mayúsculas/minúsculas, con o sin tildes, y por nombre parcial"
        )
        
        st.markdown("---")  # Separador visual
        
        # Filtro de posiciones (con traducciones al español)
        st.markdown("### ⚽ Posición en el Campo")
        posiciones_disponibles = posiciones_lista[:50]  # Top 50 posiciones
        posiciones_traducidas = [TRADUCCIONES_POSICIONES_SIMPLE.get(pos, pos) for pos in posiciones_disponibles]
        posiciones_seleccionadas_es = st.multiselect(
            "Selecciona posiciones:",
            options=posiciones_traducidas,
            default=None,
            placeholder="Selecciona una o más posiciones"
        )
        # Convertir de español a inglés para la API
        posiciones_seleccionadas = []
        if posiciones_seleccionadas_es:
            inverso_posiciones = {v: k for k, v in TRADUCCIONES_POSICIONES_SIMPLE.items()}
            posiciones_seleccionadas = [inverso_posiciones.get(pos, pos) for pos in posiciones_seleccionadas_es]
        
        # Filtro de nacionalidades (con traducciones al español)
        st.markdown("### 🌍 Nacionalidad")
        nacionalidades_disponibles = nacionalidades_lista[:30]  # Top 30
        nacionalidades_traducidas = [TRADUCCIONES_NACIONALIDADES.get(nac, nac) for nac in nacionalidades_disponibles]
        nacionalidades_seleccionadas_es = st.multiselect(
            "Selecciona nacionalidades:",
            options=nacionalidades_traducidas,
            default=None,
            placeholder="Selecciona uno o más países"
        )
        # Convertir de español a inglés para la API
        nacionalidades_seleccionadas = []
        if nacionalidades_seleccionadas_es:
            inverso_nacionalidades = {v: k for k, v in TRADUCCIONES_NACIONALIDADES.items()}
            nacionalidades_seleccionadas = [inverso_nacionalidades.get(nac, nac) for nac in nacionalidades_seleccionadas_es]
        
        # Filtro de edad
        edad_min = st.slider("Edad mínima:", 16, 45, 18)
        edad_max = st.slider("Edad máxima:", 16, 45, 35)
        
        # Filtro de valoración
        overall_min = st.slider("Valoración mínima:", 40, 95, 70)
        
        # Filtro de potencial
        potencial_min = st.slider("Potencial mínimo:", 40, 95, 70)
        
        # Filtro de valor de mercado (rango min-max)
        st.markdown("**💰 Valor de Mercado (millones €):**")
        valor_rango_millones = st.slider(
            "Rango de valor:",
            min_value=0.0,
            max_value=200.0,
            value=(0.0, 50.0),
            step=0.5,
            label_visibility="collapsed"
        )
        st.caption(f"Mínimo: €{valor_rango_millones[0]:.1f}M  —  Máximo: €{valor_rango_millones[1]:.1f}M")
        
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
        
        # ⚽ FILTRO POR NOMBRE (NUEVO)
        if nombre_busqueda and nombre_busqueda.strip():
            params["nombre"] = nombre_busqueda.strip()
        
        if posiciones_seleccionadas:
            params["posiciones_jugador"] = posiciones_seleccionadas
        if nacionalidades_seleccionadas:
            params["nacionalidad"] = nacionalidades_seleccionadas
        if edad_min:
            params["edad_min"] = edad_min
        if edad_max:
            params["edad_max"] = edad_max
        if overall_min:
            params["valoracion_min"] = overall_min
        if potencial_min:
            params["potencial_min"] = potencial_min
        
        # Filtro de valor de mercado con rango min-max (nombres corregidos)
        if valor_rango_millones[0] > 0:
            params["valor_min_eur"] = valor_rango_millones[0] * 1_000_000
        if valor_rango_millones[1] < 200.0:
            params["valor_max_eur"] = valor_rango_millones[1] * 1_000_000
        
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
            
            # Traducir posiciones en el DataFrame
            df_mostrar['posiciones_jugador'] = df_mostrar['posiciones_jugador'].apply(traducir_posicion)
            
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
                /* FORZAR BLANCO EN TODO - LIGHT MODE FIX */
                .main * {
                    color: #ffffff !important;
                }
                
                .element-container * {
                    color: #ffffff !important;
                }
                
                [data-testid="stMarkdown"] * {
                    color: #ffffff !important;
                }
                
                /* Headers de columnas SIEMPRE blancos */
                .main strong,
                .main b {
                    color: #ffffff !important;
                }
                
                /* Estilos generales de la tabla */
                .tabla-header {
                    background: linear-gradient(135deg, #304878 0%, #1a2844 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    font-weight: bold;
                    color: #ffffff !important;
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
            col_headers = st.columns([0.5, 0.8, 2, 0.7, 0.7, 1.5, 1.5, 1.5, 1, 1, 1.2])
            headers = ["#", "Foto", "Nombre", "Edad", "Año FIFA", "Nacionalidad", "Club", "Liga", "Posición", "Overall", "Potencial"]
            
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
                        
                        # Obtener foto en miniatura del jugador
                        img_miniatura = obtener_foto_jugador(jugador_id, año_jugador)
                        
                        # Convertir imagen a base64 para incrustar en HTML
                        if img_miniatura:
                            img_miniatura.thumbnail((60, 60), Image.Resampling.LANCZOS)
                            buffered = BytesIO()
                            img_miniatura.save(buffered, format="PNG")
                            img_base64 = base64.b64encode(buffered.getvalue()).decode()
                            img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 60px; height: 60px; border-radius: 8px; display: block; margin: 0 auto 8px auto;">'
                        else:
                            # Fallback con ícono genérico
                            img_html = f'''
                                <div style='
                                    width: 60px;
                                    height: 60px;
                                    background: linear-gradient(135deg, {COLOR_ACENTO_2} 0%, {COLOR_PRIMARIO} 100%);
                                    border-radius: 8px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: 30px;
                                    margin: 0 auto 8px auto;
                                '>⚽</div>
                            '''
                        
                        # Div solo con la foto (sin texto)
                        foto_html = f"""
                            <div style='
                                text-align: center;
                                margin-bottom: 6px;
                            '>
                                {img_html}
                            </div>
                        """
                        
                        st.markdown(foto_html, unsafe_allow_html=True)
                        
                        # Botón compacto y elegante con solo "Ficha"
                        if st.button("Ficha", key=f"btn_hidden_{idx_global}_{jugador_id}", type="primary", use_container_width=True):
                            st.session_state.modal_jugador_id = jugador_id
                            st.session_state.modal_jugador_nombre = nombre
                            st.session_state.modal_jugador_año = año_jugador
                            st.session_state.mostrar_modal = True
                            st.session_state.modal_clic_reciente = True
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
                        nacionalidad_tabla = jugador.get('nacionalidad', 'N/A')
                        pais_iso_tabla = obtener_codigo_iso_pais(nacionalidad_tabla)
                        bandera_url_tabla = f"https://flagcdn.com/24x18/{pais_iso_tabla}.png"
                        st.markdown(f"""
                        <div style='text-align: center;'>
                            <img src="{bandera_url_tabla}" style="width: 24px; height: 18px; display: block; margin: 0 auto 4px auto; border-radius: 3px;" onerror="this.style.display='none'">
                            <span class='jugador-stat'>{nacionalidad_tabla}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_vals[6]:
                        club = jugador.get('club', 'N/A')
                        escudo_club = obtener_escudo_club(club)
                        if escudo_club == "⚽":
                            st.markdown(f"<div style='color: #7890a8;'>{escudo_club} {club}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <img src="{escudo_club}" style="width: 24px; height: 24px; object-fit: contain;" onerror="this.style.display='none'">
                                <span style='color: #7890a8;'>{club}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col_vals[7]:
                        liga = jugador.get('liga', 'N/A')
                        escudo_liga = obtener_escudo_liga(liga)
                        if escudo_liga == "🏆":
                            st.markdown(f"<div style='color: #7890a8; font-size: 0.9em;'>{escudo_liga} {liga}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <img src="{escudo_liga}" style="width: 24px; height: 24px; object-fit: contain;" onerror="this.style.display='none'">
                                <span style='color: #7890a8; font-size: 0.9em;'>{liga}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col_vals[8]:
                        posicion = traducir_posicion(jugador.get('posiciones_jugador', 'N/A'))
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
        
        # JUGADOR MÁS VALIOSO - FICHA DESTACADA TIPO TARJETA
        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; margin: 30px 0 20px 0;'>
            <h2 style='color: {COLOR_DESTACADO}; font-size: 36px; font-weight: 800; text-transform: uppercase; 
                 letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                ⭐ JUGADOR MÁS VALIOSO DEL DATASET
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Selector de año más visible
        col_left_space, col_selector_center, col_right_space = st.columns([1, 2, 1])
        with col_selector_center:
            años_disponibles = list(range(2021, 2014, -1))
            año_seleccionado_top = st.selectbox(
                "🎯 Selecciona el año FIFA para ver al jugador más valioso",
                options=["🌍 Todos los años"] + [f"📅 {año}" for año in años_disponibles],
                key="año_jugador_top",
                help="Elige un año específico o todos los años del dataset"
            )
            
            # Extraer el año numérico
            if año_seleccionado_top == "🌍 Todos los años":
                año_filtro = None
            else:
                año_filtro = int(año_seleccionado_top.split()[-1])
        
        # Obtener jugador más valioso según filtro
        try:
            if año_filtro is None:
                url_top = f"{API_BASE_URL}/eda/jugador_mas_valioso"
            else:
                url_top = f"{API_BASE_URL}/eda/jugador_mas_valioso?año={año_filtro}"
            
            response_top = sesion_http.get(url_top, timeout=5)
            if response_top.status_code == 200:
                jugador_top = response_top.json()
            else:
                jugador_top = stats.get("jugador_mas_valioso", {})
        except:
            jugador_top = stats.get("jugador_mas_valioso", {})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if jugador_top:
            # Preparar datos
            id_sofifa = jugador_top.get("id_sofifa")
            año_datos = jugador_top.get("año_datos", 2021)
            nacionalidad = jugador_top.get("nacionalidad", "Unknown")
            pais_iso = obtener_codigo_iso_pais(nacionalidad)
            bandera_url = f"https://flagcdn.com/48x36/{pais_iso}.png"
            valor_millones = jugador_top.get('valor_eur', 0) / 1_000_000
            # Traducir posición
            posicion_traducida = traducir_posicion(jugador_top.get('posicion', 'N/A'))
            
            # Obtener foto del jugador
            img_jugador = None
            if id_sofifa:
                img_jugador = obtener_foto_jugador(id_sofifa, año_datos)
            
            # Convertir imagen a base64 para incrustar en HTML
            img_base64 = ""
            if img_jugador:
                buffered = BytesIO()
                img_jugador.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # TARJETA GRANDE TIPO FICHA PROFESIONAL
            # Usar format() en lugar de f-strings para evitar problemas con comillas
            if img_base64:
                html_foto = '<img src="data:image/png;base64,{}" style="width: 220px; height: 220px; border-radius: 20px; border: 5px solid white; box-shadow: 0 10px 30px rgba(0,0,0,0.4); object-fit: cover;">'.format(img_base64)
            else:
                html_foto = '<div style="width: 220px; height: 220px; background: linear-gradient(135deg, {} 0%, {} 100%); border-radius: 20px; border: 5px solid white; display: flex; align-items: center; justify-content: center; font-size: 80px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">⚽</div>'.format(COLOR_PRIMARIO, COLOR_ACENTO_2)
            
            html_tarjeta = """
            <style>
                .player-card-container {{
                    background: linear-gradient(135deg, {0} 0%, {1} 50%, {0} 100%);
                    border-radius: 25px;
                    padding: 30px;
                    box-shadow: 0 20px 60px rgba(255, 167, 38, 0.6);
                    position: relative;
                    overflow: hidden;
                    border: 3px solid {2};
                    margin: 20px 0;
                    min-height: 450px;
                }}
                .player-card-grid {{
                    display: flex;
                    flex-direction: row;
                    gap: 30px;
                    align-items: flex-start;
                    position: relative;
                    z-index: 1;
                }}
                .player-photo-section {{
                    flex: 0 0 auto;
                    text-align: center;
                    min-width: 200px;
                }}
                .player-info-section {{
                    flex: 1 1 auto;
                    min-width: 0;
                }}
                .player-name {{
                    color: white;
                    font-size: clamp(28px, 5vw, 48px);
                    font-weight: 900;
                    margin: 0 0 15px 0;
                    text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
                    line-height: 1.2;
                    word-wrap: break-word;
                }}
                .stats-container {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                    flex-wrap: wrap;
                }}
                .stat-badge {{
                    padding: 10px 20px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: clamp(14px, 2vw, 18px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                    white-space: nowrap;
                }}
                @media (max-width: 768px) {{
                    .player-card-grid {{
                        flex-direction: column;
                        align-items: center;
                    }}
                    .player-photo-section {{
                        margin-bottom: 20px;
                    }}
                    .player-card-container {{
                        padding: 20px;
                        min-height: auto;
                    }}
                }}
            </style>
            <div class="player-card-container">
                <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: rgba(255,255,255,0.1); border-radius: 50%; z-index: 0;"></div>
                <div style="position: absolute; bottom: -30px; left: -30px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; z-index: 0;"></div>
                
                <div class="player-card-grid">
                    <div class="player-photo-section">
                        {3}
                        <div style="margin-top: 15px; background: white; padding: 10px 20px; border-radius: 15px; display: inline-block; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                            <p style="color: {2}; font-size: 16px; font-weight: 700; margin: 0;">
                                📅 FIFA {4}
                            </p>
                        </div>
                    </div>
                    
                    <div class="player-info-section">
                        <h1 class="player-name">{5}</h1>
                        
                        <div style="display: flex; align-items: center; margin-bottom: 15px; flex-wrap: wrap;">
                            <img src="{6}" style="width: 40px; height: 30px; border-radius: 5px; margin-right: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.3);" onerror="this.style.display='none'">
                            <span style="color: white; font-size: clamp(18px, 3vw, 24px); font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.4);">
                                {7}
                            </span>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.95); padding: 15px 20px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                            <p style="color: {2}; font-size: clamp(16px, 2.5vw, 20px); font-weight: 700; margin: 0 0 8px 0;">
                                🏆 {8}
                            </p>
                            <p style="color: {9}; font-size: clamp(14px, 2vw, 16px); font-weight: 600; margin: 0;">
                                📍 {10} • {11} años
                            </p>
                        </div>
                        
                        <div class="stats-container">
                            <div class="stat-badge" style="background: {2}; color: white;">
                                ⚽ Overall: {12}
                            </div>
                            <div class="stat-badge" style="background: {13}; color: white;">
                                🚀 Potencial: {14}
                            </div>
                        </div>
                        
                        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 15px 25px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.5); border: 3px solid white;">
                            <p style="color: {2}; font-size: clamp(12px, 2vw, 16px); font-weight: 600; margin: 0 0 8px 0; text-transform: uppercase; letter-spacing: 1px;">
                                💰 Valor de Mercado
                            </p>
                            <p style="color: {2}; font-size: clamp(28px, 5vw, 42px); font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                                €{15:.1f}M
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """.format(
                COLOR_DESTACADO,  # 0
                COLOR_ADVERTENCIA,  # 1
                COLOR_PRIMARIO,  # 2
                html_foto,  # 3
                año_datos,  # 4
                jugador_top.get('nombre', 'N/A'),  # 5
                bandera_url,  # 6
                nacionalidad,  # 7
                jugador_top.get('club', 'N/A'),  # 8
                COLOR_ACENTO_2,  # 9
                posicion_traducida,  # 10
                jugador_top.get('edad', 'N/A'),  # 11
                jugador_top.get('valoracion', 'N/A'),  # 12
                COLOR_ACENTO_1,  # 13
                jugador_top.get('potencial', 'N/A'),  # 14
                valor_millones  # 15
            )
            
            # Usar st.components.v1.html para renderizar HTML complejo responsive
            # Altura adaptable: más alta en escritorio, más compacta en móvil
            components.html(html_tarjeta, height=600, scrolling=True)
    
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
        
        # Colores más vibrantes y contrastantes para el gráfico de pastel
        colores_pastel = ['#1E88E5', '#FFA726', '#66BB6A', '#AB47BC', '#FF5252', '#29B6F6', '#FFCA28', '#26A69A']
        
        fig_posiciones = px.pie(
            df_posiciones,
            values="cantidad",
            names="categoria",
            title="⚽ Distribución de Jugadores por Posición",
            color_discrete_sequence=colores_pastel,
            hole=0.4  # Crear un gráfico tipo donut para mejor visualización
        )
        
        fig_posiciones.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#FFFFFF', width=3))  # Borde blanco en cada sector
        )
        
        fig_posiciones.update_layout(
            paper_bgcolor=COLOR_PRIMARIO,
            plot_bgcolor=COLOR_PRIMARIO,
            font=dict(color="white", size=14, family="Arial"),
            title_font=dict(size=18, color=COLOR_DESTACADO, family="Arial Black"),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0.1)",
                font=dict(color="white")
            ),
            margin=dict(l=10, r=10, t=50, b=80)
        )
        
        st.plotly_chart(fig_posiciones, use_container_width=True)
    
    st.markdown("---")
    
    # OPORTUNIDADES DE MERCADO
    st.subheader("💎 Oportunidades de Mercado")
    
    # Inicializar estados de paginación
    if 'pagina_infravalorados' not in st.session_state:
        st.session_state.pagina_infravalorados = 1
    if 'pagina_sobrevalorados' not in st.session_state:
        st.session_state.pagina_sobrevalorados = 1
    
    col_oport1, col_oport2 = st.columns(2)
    
    # ========== INFRAVALORADOS ==========
    with col_oport1:
        st.markdown("##### 💚 Jugadores Infravalorados")
        
        try:
            response_infra = sesion_http.get(API_URL_INFRAVALORADOS, params={"top": 50}, timeout=30)
            if response_infra.status_code == 200:
                data_infra = response_infra.json()
                jugadores_infra = data_infra.get("top_jugadores", [])
                
                if jugadores_infra:
                    # Paginación
                    items_por_pagina = 5
                    inicio = (st.session_state.pagina_infravalorados - 1) * items_por_pagina
                    fin = inicio + items_por_pagina
                    jugadores_pagina = jugadores_infra[inicio:fin]
                    total_paginas = (len(jugadores_infra) + items_por_pagina - 1) // items_por_pagina
                    
                    # Mostrar jugadores
                    for i, jug in enumerate(jugadores_pagina, inicio + 1):
                        jugador_id = jug.get('id_sofifa')  # Corregido: usar id_sofifa
                        
                        # Extraer año de la URL de sofifa (ej: /170002 -> año 17 -> 2017)
                        url_jugador = jug.get('url_jugador', '')
                        año_jugador = 2021  # Por defecto
                        if url_jugador:
                            import re
                            match = re.search(r'/(\d{2})(\d{4})$', url_jugador)
                            if match:
                                año_fifa = int(match.group(1))
                                # Convertir código FIFA a año (17 -> 2017, 18 -> 2018, etc)
                                if año_fifa < 50:  # Asumimos años 20xx
                                    año_jugador = 2000 + año_fifa
                                else:  # Años 19xx
                                    año_jugador = 1900 + año_fifa
                        
                        foto_url = ''  # API no devuelve foto en este endpoint
                        nombre = jug.get('nombre_corto', 'N/A')
                        
                        # Contenedor con estilo
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(39, 174, 96, 0.1) 0%, rgba(46, 204, 113, 0.05) 100%);
                             padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #27ae60;'>
                        """, unsafe_allow_html=True)
                        
                        col_foto, col_info, col_btn = st.columns([1, 3, 1])
                        
                        with col_foto:
                            # Reutilizar el mismo código de foto de la lista de resultados
                            if foto_url and foto_url not in ['N/A', '', 'nan']:
                                img_html = f'<img src="{foto_url}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #27ae60;">'
                            else:
                                img_html = '<div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); display: flex; align-items: center; justify-content: center; font-size: 24px; border: 2px solid #27ae60;">⚽</div>'
                            
                            foto_html = f"""
                            <div style='display: flex; justify-content: center; align-items: center; height: 100%;'>
                                {img_html}
                            </div>
                            """
                            st.markdown(foto_html, unsafe_allow_html=True)
                        
                        with col_info:
                            club_infra = jug.get('club', 'N/A')
                            escudo_club_infra = obtener_escudo_club(club_infra)
                            club_icon_infra = f'<img src="{escudo_club_infra}" style="width: 18px; height: 18px; vertical-align: middle; object-fit: contain;" onerror="this.style.display=\'none\'">' if escudo_club_infra != "⚽" else "⚽"
                            st.markdown(f"**{i}. {nombre}** ({club_icon_infra} {club_infra})", unsafe_allow_html=True)
                            st.write(f"Real: €{jug.get('valor_mercado_eur', 0):,.0f} → Predicho: €{jug.get('valor_predicho_eur', 0):,.0f}")
                            st.write(f"💰 Diferencia: +{jug.get('diferencia_porcentual', 0):.1f}%")
                        
                        with col_btn:
                            if st.button("Ficha", key=f"btn_infra_{jugador_id}", type="primary", use_container_width=True):
                                st.session_state.modal_jugador_id = jugador_id
                                st.session_state.modal_jugador_nombre = nombre
                                st.session_state.modal_jugador_año = año_jugador
                                st.session_state.mostrar_modal = True
                                st.session_state.modal_clic_reciente = True
                                st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Controles de paginación
                    st.markdown("---")
                    col_pag1, col_pag2, col_pag3 = st.columns([1, 2, 1])
                    with col_pag1:
                        if st.button("⬅️ Anterior", disabled=(st.session_state.pagina_infravalorados == 1), key="prev_infra"):
                            st.session_state.pagina_infravalorados -= 1
                            st.rerun()
                    with col_pag2:
                        st.markdown(f"<p style='text-align: center;'>Página {st.session_state.pagina_infravalorados} de {total_paginas}</p>", unsafe_allow_html=True)
                    with col_pag3:
                        if st.button("Siguiente ➡️", disabled=(st.session_state.pagina_infravalorados == total_paginas), key="next_infra"):
                            st.session_state.pagina_infravalorados += 1
                            st.rerun()
                else:
                    st.info("No hay jugadores infravalorados en este momento")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # ========== SOBREVALORADOS ==========
    with col_oport2:
        st.markdown("##### 🔴 Jugadores Sobrevalorados")
        
        try:
            response_sobre = sesion_http.get(API_URL_SOBREVALORADOS, params={"top": 50}, timeout=30)
            if response_sobre.status_code == 200:
                data_sobre = response_sobre.json()
                jugadores_sobre = data_sobre.get("top_jugadores", [])
                
                if jugadores_sobre:
                    # Paginación
                    items_por_pagina = 5
                    inicio = (st.session_state.pagina_sobrevalorados - 1) * items_por_pagina
                    fin = inicio + items_por_pagina
                    jugadores_pagina = jugadores_sobre[inicio:fin]
                    total_paginas = (len(jugadores_sobre) + items_por_pagina - 1) // items_por_pagina
                    
                    # Mostrar jugadores
                    for i, jug in enumerate(jugadores_pagina, inicio + 1):
                        jugador_id = jug.get('id_sofifa')  # Corregido: usar id_sofifa
                        
                        # Extraer año de la URL de sofifa (ej: /210008 -> año 21 -> 2021)
                        url_jugador = jug.get('url_jugador', '')
                        año_jugador = 2021  # Por defecto
                        if url_jugador:
                            import re
                            match = re.search(r'/(\d{2})(\d{4})$', url_jugador)
                            if match:
                                año_fifa = int(match.group(1))
                                # Convertir código FIFA a año (17 -> 2017, 18 -> 2018, 21 -> 2021, etc)
                                if año_fifa < 50:  # Asumimos años 20xx
                                    año_jugador = 2000 + año_fifa
                                else:  # Años 19xx
                                    año_jugador = 1900 + año_fifa
                        
                        foto_url = ''  # API no devuelve foto en este endpoint
                        nombre = jug.get('nombre_corto', 'N/A')
                        
                        # Contenedor con estilo
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(192, 57, 43, 0.05) 100%);
                             padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #e74c3c;'>
                        """, unsafe_allow_html=True)
                        
                        col_foto, col_info, col_btn = st.columns([1, 3, 1])
                        
                        with col_foto:
                            # Reutilizar el mismo código de foto
                            if foto_url and foto_url not in ['N/A', '', 'nan']:
                                img_html = f'<img src="{foto_url}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #e74c3c;">'
                            else:
                                img_html = '<div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); display: flex; align-items: center; justify-content: center; font-size: 24px; border: 2px solid #e74c3c;">⚽</div>'
                            
                            foto_html = f"""
                            <div style='display: flex; justify-content: center; align-items: center; height: 100%;'>
                                {img_html}
                            </div>
                            """
                            st.markdown(foto_html, unsafe_allow_html=True)
                        
                        with col_info:
                            club_sobre = jug.get('club', 'N/A')
                            escudo_club_sobre = obtener_escudo_club(club_sobre)
                            club_icon_sobre = f'<img src="{escudo_club_sobre}" style="width: 18px; height: 18px; vertical-align: middle; object-fit: contain;" onerror="this.style.display=\'none\'">' if escudo_club_sobre != "⚽" else "⚽"
                            st.markdown(f"**{i}. {nombre}** ({club_icon_sobre} {club_sobre})", unsafe_allow_html=True)
                            st.write(f"Real: €{jug.get('valor_mercado_eur', 0):,.0f} → Predicho: €{jug.get('valor_predicho_eur', 0):,.0f}")
                            st.write(f"📉 Diferencia: {jug.get('diferencia_porcentual', 0):.1f}%")
                        
                        with col_btn:
                            if st.button("Ficha", key=f"btn_sobre_{jugador_id}", type="primary", use_container_width=True):
                                st.session_state.modal_jugador_id = jugador_id
                                st.session_state.modal_jugador_nombre = nombre
                                st.session_state.modal_jugador_año = año_jugador
                                st.session_state.mostrar_modal = True
                                st.session_state.modal_clic_reciente = True
                                st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Controles de paginación
                    st.markdown("---")
                    col_pag1, col_pag2, col_pag3 = st.columns([1, 2, 1])
                    with col_pag1:
                        if st.button("⬅️ Anterior", disabled=(st.session_state.pagina_sobrevalorados == 1), key="prev_sobre"):
                            st.session_state.pagina_sobrevalorados -= 1
                            st.rerun()
                    with col_pag2:
                        st.markdown(f"<p style='text-align: center;'>Página {st.session_state.pagina_sobrevalorados} de {total_paginas}</p>", unsafe_allow_html=True)
                    with col_pag3:
                        if st.button("Siguiente ➡️", disabled=(st.session_state.pagina_sobrevalorados == total_paginas), key="next_sobre"):
                            st.session_state.pagina_sobrevalorados += 1
                            st.rerun()
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
                pie_preferido_es = st.selectbox("Pie Preferido:", ["Derecho", "Izquierdo"])
                pie_preferido = "Right" if pie_preferido_es == "Derecho" else "Left"
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

# ============================================================================
# MODAL GLOBAL (funciona en cualquier tab)
# ============================================================================
if st.session_state.get('mostrar_modal', False):
    mostrar_modal_jugador(
        st.session_state.get('modal_jugador_id'),
        st.session_state.get('modal_jugador_nombre', 'Jugador'),
        st.session_state.get('modal_jugador_año', 'N/A')
    )

# FOOTER
st.markdown("---")
st.caption("© 2025 - Sistema de Scouting Inteligente FIFA | Powered by FastAPI + Streamlit + Random Forest ML")
