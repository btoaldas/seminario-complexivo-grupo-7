import streamlit as st
import pandas as pd
import plotly.express as px

# titulo
st.title("Dashboard de Videojuegos")

# ruta de los datos
DATA_PATH = r"C:\Users\fnaje\OneDrive\Documents\UniAndes\2do Seminario\seminario-proyecto-demo-games\data\processed\games_clean.csv"

# cargar datos
@st.cache_data
def cargar_datos(path):
    return pd.read_csv(path)


games_clean = cargar_datos(DATA_PATH)

# Filtros
# barra lateral
st.sidebar.header("Filtros interactivos")

generos = sorted(games_clean["genre"].unique())

# selector 
genero_seleccionado = st.sidebar.selectbox(
    "Selecciona un género:", 
    generos
)


# Tabla #1
st.header("Dataset de videojuegos")
st.write(f"Dataset completo, filtrando el género: {genero_seleccionado}")

games_filtrado = games_clean[games_clean["genre"] == genero_seleccionado]

st.dataframe(games_filtrado)



# histograma #1
st.header("Distribución de datos")

st.subheader("Distribución de ventas totales por género")

fig_hist_vt_genero = px.histogram(
    games_filtrado, 
    x="total_sales", 
    nbins=35, 
    title=f"Distribución de ventas totales para {genero_seleccionado}"
)

st.plotly_chart(fig_hist_vt_genero, use_container_width=True)

# histograma #2
st.subheader("Distribución de 'Critic Score'")

fig_hist_cs_genero = px.histogram(
    games_filtrado, 
    x="critic_score", 
    nbins=35, 
    title=f"Distribución de puntuaciones de críticos para {genero_seleccionado}"
)

st.plotly_chart(fig_hist_cs_genero, use_container_width=True)


# histograma #3
st.subheader("Distribución de 'User Score'")

fig_hist_us_genero = px.histogram(
    games_filtrado, 
    x="user_score", 
    nbins=35, 
    title=f"Distribución de puntuaciones de usuarios para {genero_seleccionado}"
)

st.plotly_chart(fig_hist_us_genero, use_container_width=True)


# Gráfico de Barras #1
st.subheader("Ventas Totales por Plataforma (Top 10)")

games_clean_platform = games_clean.groupby("platform")["total_sales"].sum().nlargest(10).reset_index()

fig_bar_platform = px.bar(
    games_clean_platform, 
    x="platform",
    y="total_sales", 
    title="Top 10 Plataformas por Ventas Totales"
)

st.plotly_chart(fig_bar_platform, use_container_width=True)


# Gráfico #1

# .Series y df para gráfico ventas por año
ventas_por_anio = games_clean.groupby("year_of_release")["total_sales"].sum()
ventas_df = ventas_por_anio.reset_index()

# header
st.header("Evolución de Ventas Totales por Año")

fig_sales_per_year = px.line(
    ventas_df, 
    x = "year_of_release", 
    y = "total_sales", 
    title="Ventas totales de videojuegos por año (Millones)",
    labels={
        "year_of_release": "Año de lanzamiento", 
        "total_sales": "Ventas Totales (Millones)"
    }, 
    markers=True
)

# mostrar figura en streamlit
st.plotly_chart(fig_sales_per_year, use_container_width=True)



# Gráfico #2
st.header("Total ventas por género en los videojuegos")

ventas_por_genero = games_clean.groupby("genre")["total_sales"].sum().sort_values(ascending=False).reset_index()

color_list = ["light_blue", "light_blue", "light_blue", "gray", "gray", "gray", "gray", "gray", "gray", "gray", "gray", "gray"]

fig_sales_genre = px.bar(
    ventas_por_genero, 
    x = "genre", 
    y = "total_sales", 
    title = "Ventas totales por género de videojuego", 
    labels={
        "genre": "Género", 
        "total_sales": "Ventas Totales (Millones)"
    }, 
    color = color_list
)

fig_sales_genre.update_layout(showlegend=False)

st.plotly_chart(fig_sales_genre, use_container_width=True)