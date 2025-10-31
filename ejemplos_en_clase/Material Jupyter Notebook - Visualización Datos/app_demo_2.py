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

# Tabla #1
st.header("Vistazo del dataset de videojuegos")
st.write("Los primeros 15 datos del dataset:")
st.dataframe(games_clean.head(15))

# .Series y df para gráfico ventas por año
ventas_por_anio = games_clean.groupby("year_of_release")["total_sales"].sum()
ventas_df = ventas_por_anio.reset_index()

# header
st.header("Evolución de Ventas Totales por Año")

# Gráfico #1
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