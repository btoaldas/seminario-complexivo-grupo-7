import streamlit as st
import time
import datetime

# titulo
st.title("Este es un título")

st.write("Este es un texto")

# la hora actual
ahora = datetime.datetime.now()

hora_formateada = ahora.strftime("%H:%M:%S")

st.write(f"Hora actual: {hora_formateada}")

st.write(f"Timestand: {time.time()}")


# st.slider() un widget deslizable
valor_slider = st.slider("Mueve este slider", 0, 100, 25)
st.write(f"El valor seleccionado es {valor_slider}")

# st.button()
if st.button("Predecir datos"):
    st.write("Se han predecido los datos")
    
st.header("Selección única: Selectbox vs. Radio")

# st.selectbox
opcion_sb = st.selectbox("¡Escoge una opción! (Selectbox)", ["Opción A", "Opción B", "Opción C"])

# st.radio
opcion_r = st.radio("¡Escoge una opción! (Radio)", ["Opción A", "Opción B", "Opción C"])

st.write(f"Selecbox: {opcion_sb}, Radio: {opcion_r}")

# st.multiselect
opciones_multi = st.multiselect(
    "Elige tu género de videojuego favorito:",
    ["Action", "Puzzle", "Stragy", "Shooter"], 
    default="Action"
)
st.write(f"Seleccionado: {opciones_multi}")


# st.slider con dos valores
st.header("Selección de rango: slider tipo tupla")

rango_anios = st.slider(
    "Selecciona un rango de años",
    2000, 2023, (2010, 2015) # valor mínimo, valor máximo, default del ragno
)
st.write(f"El slider devuelve una tupla: {rango_anios}")


# st.code
st.write("Aquí estoy mostrando un código de Pandas")
st.code(
    "pd.read_csv(ruta)", 
    language="python"
)

# elementos de notificaciones
st.header("Notificaciones")

# notificaciones visuales
st.success("Los datos fueron cargados correctamente!")
st.warning("El dataset tiene valores nulos")
st.error("No se pudo conectar a la base de datos")

# st.metric
st.metric(
    label="Ventas Totales", 
    value="$1,250,000",
    delta="$50,000 vs mes anterior"
)