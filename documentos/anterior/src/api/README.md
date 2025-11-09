# API de Valoración de Jugadores (FastAPI)

Servicio de inferencia que estima el valor de mercado de un jugador profesional usando el modelo entrenado en `notebooks/modelo_ml.ipynb`.

## Artefactos requeridos

Colocar los siguientes archivos en `models/` (ya existen en el repo):
- `modelo_valoracion_fifa.pkl`
- `columnas_modelo.pkl`

> Nota: El encoder no es necesario en inferencia. La API realiza el one-hot encoding manualmente con las mismas categorías del entrenamiento.

## Ejecutar localmente

```
# (opcional) crear entorno
python -m venv .venv && source .venv/bin/activate
pip install -r src/api/requirements.txt

# correr servidor
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Ejecutar con Docker

```
# construir imagen
docker build -t scouting-fifa-api .

# ejecutar (puerto 8000)
docker run --rm -p 8000:8000 scouting-fifa-api
```

Si prefieres montar los artefactos en tiempo de ejecución:

```
docker run --rm -p 8000:8000 -v $(pwd)/models:/app/models scouting-fifa-api
```

## Endpoints

- `GET /health` – disponibilidad del servicio.
- `POST /predict` – predice el valor en EUR.
- `POST /predict_batch` – predice varios jugadores a la vez.
- `GET /oportunidades_infravaloradas` – Top N jugadores infravalorados (predicho > real) usando `data/processed/fifa_limpio.csv`.
- `POST /resumen_valor` – entrada mínima (posición, edad, calificación, valor_real) y respuesta compacta con etiqueta OPORTUNIDAD/SOBREPRECIO.
- `GET /top_sobrevalorados` – Top N jugadores sobrevalorados (real > predicho) usando `data/processed/fifa_limpio.csv`.
- `POST /evaluate` – predice y clasifica (INFRAVALORADO/SOBREVALORADO/BIEN VALORADO).
- `GET /sample_request` – devuelve ejemplos listos para copiar/pegar para `/predict` y `/evaluate` (paginado).
 - `POST /compare` – compara 2–5 jugadores (predicción, diferencia vs valor_real y ranking por más infravalorado).
- `GET /players/search` – búsqueda filtrada por `posicion`, `min_edad`, `max_edad`, `potencial_min` (mínimo) y `potencial_max` (máximo); orden solo por `valor` con `order` (asc|desc) y paginación (`page`, `page_size`).
  - Si no hay coincidencias, responde 404 con `{"detail": "No se encontraron jugadores con los criterios proporcionados"}`.
- `GET /players/summary` – resumen estadístico (promedios y conteos) para los mismos filtros que `/players/search`.
- `GET /players/{player_id}/profile` – perfil completo de un jugador incluyendo valor predicho por el modelo.

### Ejemplo de entrada

```json
{
  "edad": 24,
  "calificacion_general": 78,
  "potencial": 84,
  "altura_cm": 180,
  "peso_kg": 75,
  "posicion_principal": "ST",
  "pie_preferido": "Right",
  "id_jugador": "abc-123",
  "nombre_corto": "L. Messi",
  "nombre_completo": "Lionel Andrés Messi"
}
```

### Respuesta

```json
{
  "id_jugador": "abc-123",
  "valor_estimado": 447717.3,
  "moneda": "EUR",
  "modelo": "RandomForestRegressor",
  "valor_estimado_formateado": "€0.45M",
  "nombre_corto": "L. Messi",
  "nombre_completo": "Lionel Andrés Messi"
}
```

## Notas de implementación

- Preprocesamiento reproducido conforme al cuaderno:
  - `imc = peso_kg / (altura_m^2)`.
  - `margen_crecimiento = potencial - calificacion_general`.
  - One‑hot de `posicion_principal` (15 categorías) y `pie_preferido` (Left/Right).
- Alineación estricta de columnas con `models/columnas_modelo.pkl`.
- Zona horaria: `America/Guayaquil`.

## Estructura

```

### `/evaluate` – Predicción + Valoración

El sistema:

1. Cargará el modelo guardado (`modelo_valoracion_fifa.pkl`)
2. Procesará los datos ingresados
3. Predecirá el valor justo estimado
4. Si el usuario ingresó el valor actual, lo comparará para clasificar:
   - Si `valor_real < valor_predicho` → INFRAVALORADO 🟢
   - Si `valor_real > valor_predicho` → SOBREVALORADO 🔴
   - Si son similares (± tolerancia) → BIEN VALORADO 🟡

Request:

```json
{
  "edad": 24,
  "calificacion_general": 78,
  "potencial": 84,
  "altura_cm": 180,
  "peso_kg": 75,
  "posicion_principal": "ST",
  "pie_preferido": "Right",
  "valor_real": 2000000,
  "tolerancia_relativa": 0.05,
  "nombre_corto": "K. De Bruyne",
  "nombre_completo": "Kevin De Bruyne"
}
```

Response:

```json
{
  "id_jugador": null,
  "valor_predicho": 49359405.49,
  "valor_real": 60000000.0,
  "clasificacion": "SOBREVALORADO",
  "diferencia": -10640594.51,
  "diferencia_relativa": 0.22,
  "moneda": "EUR",
  "valor_predicho_formateado": "€49.36M",
  "valor_real_formateado": "€60.00M",
  "diferencia_formateada": "-€10.64M",
  "nombre_corto": "K. De Bruyne",
  "nombre_completo": "Kevin De Bruyne"
}
```
src/api/
  ├─ README.md
  ├─ inference.py
  ├─ main.py
  ├─ requirements.txt
  └─ schemas.py
```

## Pruebas

```
pip install -r src/api/requirements.txt
pip install pytest
pytest -q
```

## Desarrollo con docker-compose (hot reload)

```
docker compose up --build

# servidor disponible en http://localhost:8000
```

## Ejemplos de `/sample_request`

Lista paginada de ejemplos que puedes copiar y pegar directamente. Admite filtro por nombre (`nombre`) que busca en `nombre_corto` y `nombre_completo`.

```
curl "http://localhost:8000/sample_request?page=1&page_size=3"
```

Respuesta (ejemplo, truncada):

```json
{
  "page": 1,
  "page_size": 3,
  "total": 10,
  "endpoints": {"predict": "/predict", "evaluate": "/evaluate"},
  "items": [
    {
      "predict": {
        "edad": 36,
        "calificacion_general": 91,
        "potencial": 91,
        "altura_cm": 170,
        "peso_kg": 72,
        "posicion_principal": "ST",
        "pie_preferido": "Left",
        "id_jugador": "J1",
        "nombre_corto": "L. Messi",
        "nombre_completo": "Lionel Andres Messi"
      },
      "evaluate": {
        "edad": 36,
        "calificacion_general": 91,
        "potencial": 91,
        "altura_cm": 170,
        "peso_kg": 72,
        "posicion_principal": "ST",
        "pie_preferido": "Left",
        "id_jugador": "J1",
        "nombre_corto": "L. Messi",
        "nombre_completo": "Lionel Andres Messi",
        "valor_real": 35000000,
        "tolerancia_relativa": 0.05
      }
    },
    { "predict": {"...": "..."}, "evaluate": {"...": "..."} },
    { "predict": {"...": "..."}, "evaluate": {"...": "..."} }
  ]
}
```

Filtrar por nombre (ej.: "Messi"):

```
curl "http://localhost:8000/sample_request?nombre=Messi&page=1&page_size=5"
```

## Rate limiting y logs

- Límite por defecto: `RATE_LIMIT_PER_MIN=60` solicitudes por IP en ventana de `RATE_LIMIT_WINDOW_SEC=60` segundos.
- Encabezado de correlación: envía `X-Request-ID` si deseas controlar el ID; la API siempre responderá con ese header.
- Logs estructurados en JSON con campos como: `request_id`, `ruta`, `dur_ms`, `status`, `batch_size` (cuando aplica).

## Oportunidades (Infravalorados)

Endpoint: `GET /oportunidades_infravaloradas`

Parámetros:
- `top_n` (int, default 20): cantidad de jugadores a devolver.
- `min_valor_real` (int, default 500000): filtra jugadores con valor real muy bajo.
- `anio` (int, opcional): filtra por año si existe en el dataset.
- `ascendente` (bool, default false): si es `true`, ordena por oportunidad de forma ascendente.

Requiere tener el dataset procesado en `data/processed/fifa_limpio.csv` y los artefactos del modelo en `models/`.

## Perfil de jugador (`/players/{player_id}/profile`)

Este endpoint resuelve el jugador exclusivamente por una columna de ID del dataset.

- Variables de entorno:
  - `PLAYER_ID_COLUMN` (default: `sofifa_id`) – columna usada para buscar el jugador.
  - `PLAYER_ID_STRICT` (default: `false`) – si es `true`, deshabilita fallbacks y solo acepta IDs existentes en `PLAYER_ID_COLUMN`.
- Si la columna no existe, la API responde 500 indicando el problema.
- Si no hay coincidencia exacta por ID, responde 404.

Ejemplos:

```
# Usando el ID por defecto (sofifa_id)
GET /players/158023/profile

# Cambiar la columna del ID (ej.: player_id)
PLAYER_ID_COLUMN=player_id uvicorn src.api.main:app --reload
GET /players/12345/profile
```

Con modo estricto activado:

```
PLAYER_ID_COLUMN=sofifa_id PLAYER_ID_STRICT=true uvicorn src.api.main:app --reload
```

Campos relevantes en la respuesta:
- `valor_real`, `valor_real_formateado`, `valor_predicho`, `valor_predicho_formateado`, `diferencia`, `diferencia_formateada`, `clasificacion`.

## Configuración con .env

Puedes crear un archivo `.env` en la raíz del proyecto para configurar variables sin modificar el compose/código.

Ejemplo `.env`:

```
# Columna usada para identificar jugadores en /players/{player_id}/profile
PLAYER_ID_COLUMN=sofifa_id
```

El `docker-compose.yml` ya incluye `env_file: .env` y la aplicación también carga `.env` automáticamente al iniciar.

## Sobrevalorados (Top con sobreprecio)

Endpoint: `GET /top_sobrevalorados`

Parámetros:
- `top_n` (int, default 20)
- `min_valor_real` (int, default 500000)
- `anio` (int, opcional)
- `ascendente` (bool, default false): si es `true`, ordena por sobreprecio de forma ascendente.

## Resumen rápido (solo 4 campos)

Endpoint: `POST /resumen_valor`

Ejemplo de cuerpo:

```json
{
  "posicion_principal": "LW",
  "edad": 32,
  "calificacion_general": 94,
  "valor_real": 95500000
}
```

Respuesta (valores en euros):

```json
{
  "posicion_principal": "LW",
  "edad": 32,
  "calificacion_general": 94,
  "valor_real": 95500000,
  "valor_predicho": 79065839,
  "etiqueta": "SOBREPRECIO",
  "diferencia_eur": 16434161,
  "porcentaje": 17.2
}
```
