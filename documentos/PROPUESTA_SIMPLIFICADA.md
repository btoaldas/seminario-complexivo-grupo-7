================================================================================
PROPUESTA SIMPLIFICADA - PROYECTO SCOUTING FIFA
================================================================================
Siguiendo el modelo EXACTO del profesor (ejercicio_en_clase)
Fecha: 8 de noviembre de 2025
================================================================================

## 🎯 OBJETIVO

Crear un sistema de scouting FIFA **SIMPLE, FUNCIONAL Y EXPLICABLE** que:
- Prediga el valor de mercado de jugadores
- Identifique jugadores infravalorados
- Sea fácil de entender y presentar

**MODELO A SEGUIR**: `ejercicio_en_clase/` (proyecto de videojuegos del profesor)

---

## 📁 ESTRUCTURA DEL PROYECTO

```
proyecto_fifa/
│
├── venv/                           # Entorno virtual (SIEMPRE activo)
│
├── datos/                          
│   ├── fifa.xlsx                   # Dataset original
│   └── fifa_limpio.csv             # Dataset procesado por pipeline
│
├── backend/                        
│   │
│   ├── main.py                     # 🔵 Pipeline de limpieza
│   ├── train.py                    # 🔵 Entrenamiento del modelo ML
│   ├── api_app.py                  # 🔵 API REST (FastAPI)
│   │
│   ├── scripts/                    # Módulos pequeños (como el profesor)
│   │   ├── data_loader.py          # Cargar datos
│   │   ├── data_cleaning.py        # Limpiar datos
│   │   ├── data_imputation.py      # Imputar valores nulos
│   │   ├── data_new_features.py    # Crear nuevas características
│   │   ├── data_saving.py          # Guardar datos procesados
│   │   ├── model_preprocessing.py  # Preparar datos para ML
│   │   ├── model_training.py       # Entrenar modelo
│   │   └── model_saving.py         # Guardar modelo entrenado
│   │
│   └── models/                     # Modelos entrenados
│       ├── modelo_fifa.joblib
│       └── encoder_fifa.joblib
│
├── frontend/                       
│   └── dashboard_app.py            # 🔵 Dashboard (Streamlit)
│
├── requirements.txt                # Dependencias
├── Dockerfile                      # Contenedor Docker
└── README.md                       # Documentación básica
```

**TOTAL**: 4 archivos principales + 8 scripts auxiliares = 12 archivos

---

## 🔵 LOS 4 ARCHIVOS PRINCIPALES

### 1. backend/main.py - Pipeline de Limpieza
**Qué hace**: Transforma `fifa.xlsx` → `fifa_limpio.csv`

```python
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import (
    seleccionar_columnas_relevantes,
    eliminar_duplicados,
    eliminar_filas_valor_cero
)
from scripts.data_imputation import (
    imputar_valores_numericos,
    imputar_porteros
)
from scripts.data_new_features import (
    crear_categoria_edad,
    crear_promedio_atributos
)
from scripts.data_saving import guardar_datos_limpios

if __name__ == "__main__":
    # PASO 1: Cargar datos
    df = cargar_datos("datos/fifa.xlsx")
    
    # PASO 2: Limpiar
    df = seleccionar_columnas_relevantes(df)
    df = eliminar_duplicados(df)
    df = eliminar_filas_valor_cero(df)
    
    # PASO 3: Imputar
    df = imputar_valores_numericos(df)
    df = imputar_porteros(df)
    
    # PASO 4: Crear features
    df = crear_categoria_edad(df)
    df = crear_promedio_atributos(df)
    
    # PASO 5: Guardar
    guardar_datos_limpios(df, "datos/fifa_limpio.csv")
```

### 2. backend/train.py - Entrenamiento ML
**Qué hace**: Entrena modelo de regresión para predecir `valor_euros`

```python
from scripts.model_preprocessing import preparar_datos_modelo, dividir_datos
from scripts.model_training import entrenar_modelo
from scripts.model_saving import guardar_modelo

if __name__ == "__main__":
    # Cargar datos limpios
    df = pd.read_csv("datos/fifa_limpio.csv")
    
    # Preparar para ML
    X, y, encoder = preparar_datos_modelo(df)
    X_train, X_test, y_train, y_test = dividir_datos(X, y)
    
    # Entrenar modelo
    modelo = entrenar_modelo(X_train, X_test, y_train, y_test)
    
    # Guardar modelo y encoder
    guardar_modelo(modelo, encoder, 
                   "models/modelo_fifa.joblib", 
                   "models/encoder_fifa.joblib")
```

### 3. backend/api_app.py - API REST
**Qué hace**: Expone endpoints para predicción y búsqueda

```python
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="API Scouting FIFA")

# Cargar modelo y datos al inicio
modelo = joblib.load("models/modelo_fifa.joblib")
encoder = joblib.load("models/encoder_fifa.joblib")
jugadores = pd.read_csv("datos/fifa_limpio.csv")

@app.get("/")
def home():
    return {"mensaje": "API Scouting FIFA"}

@app.get("/jugadores/buscar")
def buscar_jugadores(posicion: str = None, edad_min: int = 16, edad_max: int = 45):
    """Busca jugadores según filtros"""
    df_filtrado = jugadores.copy()
    
    if posicion:
        df_filtrado = df_filtrado[df_filtrado['posicion_principal'] == posicion]
    
    df_filtrado = df_filtrado[
        (df_filtrado['edad'] >= edad_min) & 
        (df_filtrado['edad'] <= edad_max)
    ]
    
    return df_filtrado.to_dict('records')

@app.post("/ml/predecir")
def predecir_valor(datos_jugador: dict):
    """Predice el valor de mercado de un jugador"""
    # Convertir datos a formato del modelo
    input_df = pd.DataFrame([datos_jugador])
    
    # Predecir
    prediccion = modelo.predict(input_df)
    
    return {
        "valor_predicho_euros": float(prediccion[0]),
        "valor_predicho_millones": round(prediccion[0] / 1_000_000, 2)
    }

@app.get("/jugadores/infravalorados")
def obtener_infravalorados(limite: int = 50):
    """Retorna jugadores cuyo valor predicho > valor real"""
    # Cargar predicciones (calculadas previamente)
    jugadores['valor_predicho'] = modelo.predict(X_procesado)
    jugadores['diferencia'] = jugadores['valor_predicho'] - jugadores['valor_euros']
    
    infravalorados = jugadores[jugadores['diferencia'] > 0].nlargest(limite, 'diferencia')
    
    return infravalorados.to_dict('records')
```

### 4. frontend/dashboard_app.py - Dashboard Interactivo
**Qué hace**: Interfaz visual para usuarios

```python
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Scouting FIFA")

st.title("⚽ Sistema de Scouting FIFA")
st.caption("Identificación de jugadores infravalorados mediante Machine Learning")

# Crear tabs
tab1, tab2, tab3 = st.tabs(["🔍 Búsqueda", "🤖 Predicción", "💎 Infravalorados"])

# ============================================================================
# TAB 1: BÚSQUEDA DE JUGADORES
# ============================================================================
with tab1:
    st.header("Búsqueda de Jugadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        posicion = st.selectbox("Posición", ["Todas", "Delantero", "Mediocampista", "Defensa", "Portero"])
    
    with col2:
        rango_edad = st.slider("Rango de edad", 16, 45, (20, 30))
    
    if st.button("Buscar"):
        # Llamar a la API
        response = requests.get(
            "http://localhost:8000/jugadores/buscar",
            params={
                "posicion": posicion if posicion != "Todas" else None,
                "edad_min": rango_edad[0],
                "edad_max": rango_edad[1]
            }
        )
        
        jugadores = response.json()
        
        # Mostrar resultados en tabla
        st.dataframe(jugadores)
        
        # Seleccionar un jugador para ver detalles
        if len(jugadores) > 0:
            st.subheader("Detalle del Jugador")
            
            jugador_seleccionado = st.selectbox(
                "Selecciona un jugador",
                [j['nombre_corto'] for j in jugadores]
            )
            
            # Obtener datos del jugador seleccionado
            jugador = next(j for j in jugadores if j['nombre_corto'] == jugador_seleccionado)
            
            # ========================================
            # TARJETA ESPECIAL DEL JUGADOR
            # ========================================
            col_foto, col_info, col_radar = st.columns([1, 1, 2])
            
            with col_foto:
                # Placeholder para foto (puedes añadir URL real)
                st.image("https://via.placeholder.com/150", width=150)
                st.markdown(f"**{jugador['nombre_completo']}**")
                st.markdown(f"🏆 {jugador['club']}")
                st.markdown(f"📍 {jugador['posicion_principal']}")
            
            with col_info:
                st.metric("Overall", jugador['calificacion_general'])
                st.metric("Potencial", jugador['potencial'])
                st.metric("Valor", f"{jugador['valor_euros']:,.0f} EUR")
                st.metric("Salario", f"{jugador['salario_euros']:,.0f} EUR")
            
            with col_radar:
                # Gráfico radar de atributos
                atributos = {
                    'Ritmo': jugador.get('ritmo', 0),
                    'Tiro': jugador.get('tiro', 0),
                    'Pase': jugador.get('pase', 0),
                    'Regate': jugador.get('regate', 0),
                    'Defensa': jugador.get('defensa', 0),
                    'Físico': jugador.get('fisico', 0)
                }
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=list(atributos.values()),
                    theta=list(atributos.keys()),
                    fill='toself',
                    line=dict(color='#667eea')
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    title="Atributos del Jugador"
                )
                
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: PREDICCIÓN DE VALOR
# ============================================================================
with tab2:
    st.header("Predictor de Valor de Mercado")
    
    with st.form("form_prediccion"):
        col1, col2 = st.columns(2)
        
        with col1:
            edad = st.slider("Edad", 16, 45, 25)
            overall = st.slider("Overall", 40, 95, 75)
            potencial = st.slider("Potencial", 40, 95, 80)
            posicion = st.selectbox("Posición", ["Delantero", "Mediocampista", "Defensa", "Portero"])
        
        with col2:
            ritmo = st.slider("Ritmo", 0, 100, 70)
            tiro = st.slider("Tiro", 0, 100, 70)
            pase = st.slider("Pase", 0, 100, 70)
            regate = st.slider("Regate", 0, 100, 70)
        
        submitted = st.form_submit_button("Predecir Valor")
    
    if submitted:
        # Preparar datos para predicción
        datos = {
            "edad": edad,
            "calificacion_general": overall,
            "potencial": potencial,
            "posicion_principal": posicion,
            "ritmo": ritmo,
            "tiro": tiro,
            "pase": pase,
            "regate": regate
        }
        
        # Llamar API
        response = requests.post("http://localhost:8000/ml/predecir", json=datos)
        resultado = response.json()
        
        # Mostrar resultado
        st.success("✅ Predicción realizada")
        st.metric(
            "Valor Estimado", 
            f"{resultado['valor_predicho_millones']} M EUR",
            delta=None
        )

# ============================================================================
# TAB 3: JUGADORES INFRAVALORADOS
# ============================================================================
with tab3:
    st.header("Oportunidades de Mercado")
    st.write("Jugadores cuyo valor predicho es mayor al valor actual")
    
    # Obtener jugadores infravalorados
    response = requests.get("http://localhost:8000/jugadores/infravalorados?limite=50")
    infravalorados = response.json()
    
    # Mostrar tabla
    st.dataframe(infravalorados)
    
    # Gráfico de barras
    df_plot = pd.DataFrame(infravalorados).head(20)
    
    fig = px.bar(
        df_plot,
        x='nombre_corto',
        y='diferencia',
        title="Top 20 Jugadores Infravalorados",
        labels={'diferencia': 'Diferencia (EUR)', 'nombre_corto': 'Jugador'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## 📦 TECNOLOGÍAS (Las mismas del profesor)

```txt
# requirements.txt
pandas==2.x
numpy==2.x
openpyxl==3.x
scikit-learn==1.3+
lightgbm==4.x          # o random forest
joblib==1.x
fastapi==0.100+
uvicorn==0.20+
streamlit==1.25+
plotly==5.x
requests==2.31+
```

---

## 🚀 FLUJO DE TRABAJO

```
1. Ejecutar pipeline:
   python backend/main.py
   → Genera: datos/fifa_limpio.csv

2. Entrenar modelo:
   python backend/train.py
   → Genera: models/modelo_fifa.joblib, models/encoder_fifa.joblib

3. Iniciar API:
   uvicorn backend.api_app:app --reload
   → API en: http://localhost:8000

4. Iniciar Dashboard:
   streamlit run frontend/dashboard_app.py
   → Dashboard en: http://localhost:8501
```

---

## ✅ CHECKLIST DE SIMPLICIDAD

- [ ] Solo 4 archivos principales (.py)
- [ ] Scripts auxiliares son cortos (< 100 líneas cada uno)
- [ ] Sin carpetas extras (src/, tests/, docs/)
- [ ] Sin librerías complejas (solo las del profesor)
- [ ] Sin clases ni POO (todo funcional)
- [ ] Código comentado en español
- [ ] snake_case en todo
- [ ] Fácil de explicar en 15-20 min

---

## 🎨 EXTRA: TARJETA ESPECIAL DEL JUGADOR

Incluye:
- ✅ Foto/imagen del jugador (placeholder o desde URL)
- ✅ Datos básicos (nombre, club, posición)
- ✅ Métricas (overall, potencial, valor, salario)
- ✅ Gráfico radar con 6 atributos principales
- ✅ Link al perfil completo (opcional)

---

## 📋 COMPARACIÓN: Videojuegos vs FIFA

| Aspecto | Videojuegos (profesor) | FIFA (nosotros) |
|---------|------------------------|-----------------|
| **Dataset** | games.csv | fifa.xlsx → fifa_limpio.csv |
| **Target** | total_sales | valor_euros |
| **Features principales** | platform, genre, year, scores | posicion, edad, overall, atributos |
| **Modelo ML** | LGBMRegressor | RandomForest o LGBMRegressor |
| **API endpoints** | 2-3 endpoints | 3 endpoints |
| **Dashboard tabs** | 2 tabs | 3 tabs |
| **Extra especial** | - | Tarjeta de jugador con radar |

---

## 🎯 ENTREGABLES FINALES

1. ✅ Código fuente completo (12 archivos .py)
2. ✅ Dataset limpio (fifa_limpio.csv)
3. ✅ Modelo entrenado (.joblib)
4. ✅ API funcional (FastAPI)
5. ✅ Dashboard interactivo (Streamlit)
6. ✅ Dockerfile
7. ✅ README.md
8. ✅ requirements.txt

---

## ⏱️ TIEMPO ESTIMADO

- Pipeline (main.py): **1-2 horas**
- ML (train.py): **1 hora**
- API (api_app.py): **1-2 horas**
- Dashboard (dashboard_app.py): **2-3 horas**
- Testing y ajustes: **1-2 horas**

**TOTAL: 6-10 horas de trabajo**

---

## 💬 NOTA FINAL

Este proyecto es **SIMPLE, DIRECTO Y FUNCIONAL**, exactamente como el del profesor.

No hay complejidad innecesaria, todo es entendible y explicable.

La única diferencia es la **tarjeta especial del jugador** que añade valor visual sin complicar el código.

================================================================================
FIN DE LA PROPUESTA SIMPLIFICADA
================================================================================
