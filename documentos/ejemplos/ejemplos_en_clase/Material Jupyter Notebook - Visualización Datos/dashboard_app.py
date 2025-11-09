import streamlit as st
import pandas as pd
import plotly.express as px

# configuración de nuestra página
st.set_page_config(layout="wide")

# ruta de los datos
DATA_PATH = r"C:\Users\fnaje\OneDrive\Documents\UniAndes\2do Seminario\seminario-proyecto-demo-games\data\processed\games_clean.csv"

# cargar datos
@st.cache_data
def cargar_datos(path):
    """función para cargar datos con caché"""
    return pd.read_csv(path)

# datos cargados
games_clean = cargar_datos(DATA_PATH)


# titulo
st.title("🎮Dashboard de Videojuegos🎮")

# para mostrar texto  con fuente pequeña
st.caption("Seminario Complexivo de Titulación | UniAndes | Profesor: Juan Felipe Nájera")

st.subheader("Análisis Exploratorio de Datos y Predicción de Ventas")

# crear pestañas
tab1, tab2 = st.tabs(["Análisis Exploratorio (EDA)", "Predicción de Ventas (ML)"])


# PESTAÑA 1
with tab1: 
    st.header("Análisis Exploratorio de Ventas")
    
    col_filtro1, col_filtro2 = st.columns(2)
    
    # filtro de géneros
    with col_filtro1:
    
        generos_lista = sorted(games_clean["genre"].unique())

        # selector 
        genero_seleccionado = st.multiselect(
            "Selecciona Géneros:", 
            options=generos_lista, 
            default=generos_lista
        )
    with col_filtro2:
        min_year = int(games_clean["year_of_release"].min())
        max_year = int(games_clean["year_of_release"].max())
        
        #st.slider
        rango_anios = st.slider(
            "Selecciona un rango de años:",
            min_value=min_year, 
            max_value=max_year, 
            value=(min_year, max_year) # valor mínimo, valor máximo, default del ragno
        )
    
    # la lógica del filtro
    # filtramos el df antes de calcular las métricas
    # se puede seleccionar uno o varios generos
    if genero_seleccionado:
        # genero
        filtro_genero = games_clean["genre"].isin(genero_seleccionado)
        
        # rango de años seleccionado
        filtro_anio = (games_clean["year_of_release"] >= rango_anios[0]) & (games_clean["year_of_release"] <= rango_anios[1])
        
        # filtro de ambos filtros
        games_filtrado = games_clean[filtro_genero & filtro_anio]
        
    else:
        # si no se selecciona ninguno, se crea un df vacío para evitar errores
        games_filtrado = pd.DataFrame(columns=games_clean.columns)
    
    if not games_filtrado.empty:
        # KPIs
        # métricas para mostrar valores numéricos grandes
        total_sales_global = games_filtrado["total_sales"].sum()
        total_videogames = games_filtrado["videogame_names"].count()
        total_platforms = games_filtrado["platform"].nunique()
        avg_critic_score = games_filtrado["critic_score"].mean()
        avg_user_score = games_filtrado["user_score"].mean()
    else:
        st.warning("No hay datos para los géneros seleccionados")
        total_sales_global = 0
        total_videogames = 0
        total_platforms = 0
        avg_critic_score = 0
        avg_user_score = 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # MÉTRICAS
    with col1:
        st.metric(
            label="Ventas Globales (Millones)", 
            value=f"$ {total_sales_global:,.0f} M"
        )
    with col2:
        st.metric(
            label="Total Videojuegos", 
            value=f"{total_videogames}"
        )
    with col3:
        st.metric(
            label="Total Consolas", 
            value=f"{total_platforms}"
        )
    with col4:
        st.metric(
            label="Puntaje Promedio de Críticos", 
            value=f"{avg_critic_score:,.1f}"
        )
    with col5:
        st.metric(
            label="Puntaje Promedio de Usuarios", 
            value=f"{avg_user_score:,.1f}"
        )
        
    st.markdown("---")
    
    # GRÁFICO VENTAS TOTALES POR REGIÓN
    st.subheader("Evolución de Ventas por Región")
    
    # df de ventas por año por region
    sales_per_region_df = games_clean.groupby("year_of_release")[
        ["na_sales", "eu_sales", "jp_sales", "other_sales"]
    ].sum().reset_index()
    
    # .melt transforma un df de "ancho" a "largo"
    sales_per_region_melt_df = sales_per_region_df.melt(
        id_vars="year_of_release", 
        value_vars=["na_sales", "eu_sales", "jp_sales", "other_sales"], 
        var_name="region", 
        value_name="sales"
    )
    
    fig_sales_per_region = px.line(
        sales_per_region_melt_df, 
        x = "year_of_release", 
        y = "sales",
        color="region", 
        title="Evolución de Ventas por Región (Millones)",
        labels={
            "year_of_release": "Año de lanzamiento", 
            "sales": "Ventas Totales (Millones)", 
            "region": "Región"
        }, 
        markers=True
    )
    
    # añadir slider 
    fig_sales_per_region.update_layout(xaxis_rangeslider_visible=True)
    
    # mostrar la figura en streamlit
    st.plotly_chart(fig_sales_per_region, use_container_width=True)
    st.caption("Filtro para mover el rango de años en el gráfico")
    
    st.markdown("---")
    st.subheader("Análisis de Plataformas y Composición del Mercado")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
    
        # Gráfico de Barras #1
        games_clean_platform = games_clean.groupby("platform")["total_sales"].sum().nlargest(10).reset_index()

        fig_bar_platform = px.bar(
            games_clean_platform, 
            x="platform",
            y="total_sales", 
            title="Top 10 Plataformas por Ventas Totales", 
            labels={
                "platform": "Plataforma", 
                "total_sales": "Ventas Totales (Millones)", 
            },
            color="total_sales", 
            color_continuous_scale="Blues", 
            text_auto=".2s"
        )
        
        fig_bar_platform.update_layout(showlegend=False, title_x=0.5, plot_bgcolor="rosybrown")

        st.plotly_chart(fig_bar_platform, use_container_width=True)
        
    with col_graf2:
        st.write("##### Composición de Ventas por Región (%)")
        
        total_na = games_filtrado["na_sales"].sum()
        total_eu = games_filtrado["eu_sales"].sum()
        total_jp = games_filtrado["jp_sales"].sum()
        total_other = games_filtrado["other_sales"].sum()
        
        data_treemap = pd.DataFrame({
            "region": ["Norteamérica", "Europa", "Japón", "Otras Regiones"], 
            "ventas": [total_na, total_eu, total_jp, total_other]
        })
        
        fig_treemap = px.treemap(
            data_treemap, 
            path=[px.Constant("Ventas Totales"), "region"], 
            values="ventas", 
            color="ventas", 
            color_continuous_scale="Blues", 
            title="Distribución de Ventas por Región (%)",
            labels={
                "ventas": "Ventas (Millones)" 
            } 
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    