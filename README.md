# 🎓 Seminario Complexivo - Grupo 7

**Autor:**  
📌 *Alberto Alexander Aldás Villacrés*
📌 *Cristian Joel Riofrio Medina*
📌 *Wilson Fernado Saavedra Álvarez*
---

## 🧠 Tema

**Predicción de jugadores infravalorados para oportunidades de negocio**

---

## 🎯 Objetivo general

Desarrollar un **sistema analítico integral** que permita **identificar jugadores de fútbol potencialmente infravalorados**, con base en su desempeño, características y evolución a lo largo del tiempo, generando información útil para la **toma de decisiones estratégicas y de negocio**.

---

## ⚙️ Objetivos específicos

1. **Diseñar e implementar un pipeline de datos robusto**  
   - Integrar y limpiar múltiples fuentes (archivos Excel de FIFA 2015–2021).  
   - Gestionar valores faltantes, duplicados y formatos inconsistentes.  
   - Normalizar variables numéricas y codificar variables categóricas.

2. **Realizar un análisis exploratorio de datos (EDA)**  
   - Identificar patrones, tendencias y correlaciones entre rendimiento y valor de mercado.  
   - Detectar posibles casos de jugadores infravalorados.

3. **Entrenar un modelo de Machine Learning (Regresión)**  
   - Predecir el valor de mercado estimado de cada jugador a partir de variables como edad, posición, goles, asistencias, potencial, rating y salario.  
   - Evaluar el rendimiento del modelo mediante métricas como **MAE** y **R²**.

4. **Desplegar el modelo como un servicio web (API)**  
   - Implementar una **API REST con FastAPI** para exponer las predicciones del modelo.  
   - Permitir la consulta dinámica de jugadores y valores estimados.

5. **Visualizar los resultados en un dashboard interactivo**  
   - Integrar el modelo y los resultados en un **dashboard en Streamlit**, que permita explorar:
     - Ranking de jugadores infravalorados.  
     - Comparativas entre ligas, posiciones y temporadas.  
     - Evolución de valor y rendimiento individual.

---