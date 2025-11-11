# DOCUMENTACIÓN DE LA API - SISTEMA SCOUTING FIFA

## Información General

**URL Base:** `http://localhost:8000`  
**Documentación Interactiva:** `http://localhost:8000/docs`  
**Versión:** 2.0.0  
**Modelo ML:** Random Forest Regressor (R² = 98.30%)

---

## Endpoints Disponibles

### 1. **GET /** - Información de la API
Retorna información general sobre la API y sus capacidades.

**Response:**
```json
{
  "nombre": "API Sistema Scouting Inteligente FIFA",
  "version": "2.0.0",
  "modelo_ml": {
    "tipo": "Random Forest Regressor",
    "r2_score": 0.9830,
    "features": 110
  },
  "endpoints_disponibles": {...}
}
```

---

### 2. **GET /jugadores/filtros** - Obtener Opciones de Filtros
Retorna todas las opciones únicas disponibles para filtros.

**Response:**
```json
{
  "posiciones": ["ST", "CM", "CB", ...],
  "nacionalidades": ["Argentina", "Brazil", ...],
  "clubes": ["FC Barcelona", "Real Madrid", ...],
  "ligas": ["Spain Primera Division", ...],
  "rangos": {
    "edad_min": 16,
    "edad_max": 45,
    "valoracion_min": 40,
    "valoracion_max": 94
  }
}
```

---

### 3. **GET /jugadores/buscar** - Buscar Jugadores
Busca jugadores aplicando filtros personalizables.

**Query Parameters:**
- `posicion` (array): Posiciones (ej: ["ST", "LW"])
- `nacionalidad` (array): Nacionalidades
- `club` (array): Clubes
- `liga` (array): Ligas
- `edad_min` (int): Edad mínima
- `edad_max` (int): Edad máxima
- `valoracion_min` (int): Valoración mínima
- `valoracion_max` (int): Valoración máxima
- `potencial_min` (int): Potencial mínimo
- `potencial_max` (int): Potencial máximo
- `valor_max_eur` (float): Valor máximo EUR
- `limite` (int): Límite de resultados (default: 100)
- `ordenar_por` (string): Campo ordenamiento
- `orden_descendente` (bool): Orden desc (default: true)

**Ejemplo:**
```
GET /jugadores/buscar?edad_min=20&edad_max=25&valoracion_min=80&limite=20
```

**Response:**
```json
{
  "total_encontrados": 150,
  "total_dataset": 122501,
  "jugadores": [
    {
      "id_sofifa": 158023,
      "nombre_corto": "L. Messi",
      "edad": 34,
      "nacionalidad": "Argentina",
      "club": "Paris Saint-Germain",
      "valoracion_global": 93,
      "valor_mercado_eur": 78000000,
      ...
    }
  ]
}
```

---

### 4. **GET /jugadores/{jugador_id}/perfil** - Perfil Completo
Retorna todos los atributos de un jugador específico más predicción ML.

**Path Parameters:**
- `jugador_id` (int): ID de SoFIFA del jugador

**Ejemplo:**
```
GET /jugadores/158023/perfil
```

**Response:**
```json
{
  "jugador": {
    "id_sofifa": 158023,
    "nombre_corto": "L. Messi",
    "nombre_completo": "Lionel Andrés Messi Cuccittini",
    "edad": 34,
    "valoracion_global": 93,
    "potencial": 93,
    "valor_mercado_eur": 78000000,
    "ritmo_velocidad": 85,
    "tiro_disparo": 92,
    "pase": 91,
    ...
  },
  "prediccion_ml": {
    "valor_predicho_eur": 82500000,
    "valor_real_eur": 78000000,
    "diferencia_eur": 4500000,
    "diferencia_porcentual": 5.77,
    "clasificacion": "Valor Justo"
  }
}
```

---

### 5. **POST /ml/predecir_valor** - Predecir Valor de Mercado
**Endpoint principal de ML** para predecir valor de jugadores (incluso no registrados).

**Request Body (todos opcionales):**
```json
{
  "edad": 25,
  "valoracion_global": 85,
  "potencial": 88,
  "ritmo_velocidad": 85,
  "tiro_disparo": 80,
  "pase": 75,
  "regate_gambeta": 82,
  "defensa": 35,
  "fisico": 70,
  "pie_debil": 4,
  "habilidades_regate": 4,
  "reputacion_internacional": 3,
  "club": "FC Barcelona",
  "liga": "Spain Primera Division",
  "posiciones_jugador": "LW, ST",
  "nacionalidad": "Brazil",
  "pie_preferido": "Right",
  "ritmo_trabajo": "High/Medium",
  "altura_cm": 175,
  "peso_kg": 68
}
```

**Response:**
```json
{
  "valor_predicho_eur": 5200000,
  "valor_predicho_formateado": "€5.20M",
  "confianza_prediccion": "Alta",
  "percentil_valor": 75,
  "categoria_valor": "Medio (Top 50%)",
  "features_utilizadas": 15,
  "features_imputadas": 95
}
```

**Casos de Uso:**
1. **Jugador completo:** Proporcionar todos los datos disponibles
2. **Jugador parcial:** Solo algunos atributos (el modelo imputa faltantes)
3. **Jugador nuevo:** Sin club/liga, solo atributos técnicos
4. **Análisis "what-if":** Cambiar valores para ver impacto

---

### 6. **GET /jugadores/infravalorados** - Top Infravalorados
Identifica oportunidades de mercado (valor predicho > valor actual).

**Query Parameters:**
- `top` (int): Cantidad de resultados (1-100, default: 10)
- `diferencia_minima_porcentual` (float): Umbral % (default: 20.0)
- `edad_maxima` (int): Edad máxima para filtrar
- `posicion` (array): Filtrar por posiciones

**Ejemplo:**
```
GET /jugadores/infravalorados?top=20&diferencia_minima_porcentual=30&edad_maxima=25
```

**Response:**
```json
{
  "total_infravalorados": 450,
  "top_jugadores": [
    {
      "id_sofifa": 234567,
      "nombre_corto": "J. Player",
      "edad": 22,
      "club": "Small Club FC",
      "valor_mercado_eur": 2000000,
      "valor_predicho_eur": 3500000,
      "diferencia_porcentual": 75.0
    }
  ]
}
```

---

### 7. **GET /jugadores/sobrevalorados** - Top Sobrevalorados
Identifica jugadores potencialmente sobrevalorados.

**Query Parameters:**
- `top` (int): Cantidad de resultados (1-100, default: 10)
- `diferencia_minima_porcentual` (float): Umbral % (default: 20.0)

**Ejemplo:**
```
GET /jugadores/sobrevalorados?top=15
```

**Response:**
```json
{
  "total_sobrevalorados": 320,
  "top_jugadores": [
    {
      "id_sofifa": 345678,
      "nombre_corto": "E. Player",
      "valor_mercado_eur": 10000000,
      "valor_predicho_eur": 6500000,
      "diferencia_porcentual": -35.0
    }
  ]
}
```

---

### 8. **GET /eda/estadisticas_generales** - Estadísticas del Dataset
Retorna KPIs generales del dataset.

**Response:**
```json
{
  "total_jugadores": 122501,
  "total_clubes": 954,
  "total_ligas": 56,
  "total_nacionalidades": 164,
  "edad_promedio": 25.3,
  "valoracion_promedio": 66.2,
  "valor_mercado_promedio_eur": 2050152,
  "jugador_mas_valioso": {
    "nombre": "K. Mbappé",
    "valor_eur": 123000000,
    "club": "Paris Saint-Germain"
  },
  "club_mas_valioso": {
    "nombre": "Manchester City",
    "valor_total_eur": 1200000000
  }
}
```

---

### 9. **GET /eda/datos_graficos** - Datos para Visualizaciones
Retorna datos agregados para gráficos del dashboard.

**Query Parameters:**
- `tipo_analisis` (string): "posiciones", "nacionalidades", "clubes", "ligas", "edades"
- `top_n` (int): Cantidad de elementos (5-50, default: 20)

**Ejemplo:**
```
GET /eda/datos_graficos?tipo_analisis=clubes&top_n=15
```

**Response:**
```json
{
  "tipo_analisis": "clubes",
  "datos": [
    {
      "club": "Manchester City",
      "valor_total_eur": 1200000000,
      "valor_promedio_eur": 35000000,
      "cantidad_jugadores": 34
    }
  ]
}
```

---

## Ejemplos de Uso Completo

### Caso 1: Buscar Delanteros Jóvenes Prometedores
```python
import requests

url = "http://localhost:8000/jugadores/buscar"
params = {
    "categoria_posicion": ["Delantero"],
    "edad_min": 18,
    "edad_max": 23,
    "potencial_min": 80,
    "valor_max_eur": 10000000,
    "limite": 50,
    "ordenar_por": "potencial",
    "orden_descendente": True
}

response = requests.get(url, params=params)
jugadores = response.json()["jugadores"]

for j in jugadores:
    print(f"{j['nombre_corto']}: Potencial {j['potencial']}, €{j['valor_mercado_eur']:,}")
```

### Caso 2: Predecir Valor de Jugador Nuevo
```python
import requests

url = "http://localhost:8000/ml/predecir_valor"
datos_jugador = {
    "edad": 21,
    "valoracion_global": 75,
    "potencial": 85,
    "ritmo_velocidad": 88,
    "tiro_disparo": 70,
    "pase": 68,
    "regate_gambeta": 80,
    "defensa": 30,
    "fisico": 65,
    "posiciones_jugador": "LW",
    "nacionalidad": "Argentina",
    "liga": "Spain Primera Division"
}

response = requests.post(url, json=datos_jugador)
prediccion = response.json()

print(f"Valor predicho: {prediccion['valor_predicho_formateado']}")
print(f"Confianza: {prediccion['confianza_prediccion']}")
print(f"Percentil: {prediccion['percentil_valor']}%")
```

### Caso 3: Identificar Oportunidades de Mercado
```python
import requests

# 1. Obtener infravalorados
url_infra = "http://localhost:8000/jugadores/infravalorados"
params = {
    "top": 20,
    "diferencia_minima_porcentual": 25,
    "edad_maxima": 26
}

response = requests.get(url_infra, params=params)
infravalorados = response.json()["top_jugadores"]

print(f"OPORTUNIDADES ENCONTRADAS: {len(infravalorados)}")
for j in infravalorados:
    print(f"{j['nombre_corto']} ({j['club']})")
    print(f"  Valor actual: €{j['valor_mercado_eur']:,}")
    print(f"  Valor predicho: €{j['valor_predicho_eur']:,}")
    print(f"  Ganancia potencial: {j['diferencia_porcentual']:.1f}%")
    print()
```

### Caso 4: Análisis Completo de Perfil
```python
import requests

# 1. Buscar jugador
url_buscar = "http://localhost:8000/jugadores/buscar"
params = {"nombre": "Haaland", "limite": 1}
jugadores = requests.get(url_buscar, params=params).json()["jugadores"]
jugador_id = jugadores[0]["id_sofifa"]

# 2. Obtener perfil completo
url_perfil = f"http://localhost:8000/jugadores/{jugador_id}/perfil"
perfil = requests.get(url_perfil).json()

# 3. Analizar
j = perfil["jugador"]
pred = perfil["prediccion_ml"]

print(f"ANÁLISIS DE: {j['nombre_corto']}")
print(f"Club: {j['club']}, Edad: {j['edad']}")
print(f"Valoración: {j['valoracion_global']}, Potencial: {j['potencial']}")
print(f"\nVALORACIÓN DE MERCADO:")
print(f"  Valor actual:   €{pred['valor_real_eur']:,}")
print(f"  Valor predicho: €{pred['valor_predicho_eur']:,}")
print(f"  Clasificación:  {pred['clasificacion']}")
```

---

## Códigos de Estado HTTP

- **200 OK:** Solicitud exitosa
- **404 Not Found:** Jugador no encontrado
- **422 Unprocessable Entity:** Datos de entrada inválidos
- **500 Internal Server Error:** Error en el servidor

---

## Límites y Consideraciones

- **Rate Limit:** No implementado (desarrollo local)
- **Tamaño Dataset:** 122,501 jugadores
- **Timeout Predicción:** ~100-300ms por jugador
- **Máximo Resultados:** 1000 jugadores por búsqueda

---

## Iniciar el Servidor

```bash
cd backend
python api_scouting_fifa.py
```

El servidor estará disponible en: `http://localhost:8000`  
Documentación interactiva: `http://localhost:8000/docs`

---

## Tecnologías Utilizadas

- **FastAPI** 0.115.5
- **Uvicorn** 0.32.1
- **Pydantic** 2.10.3
- **Pandas** 2.2.0
- **NumPy** 2.2.0
- **Scikit-learn** 1.5.2
- **Joblib** 1.4.2
