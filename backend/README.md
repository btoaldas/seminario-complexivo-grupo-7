# API REST - SISTEMA SCOUTING FIFA

## Inicio Rápido

### 1. Iniciar la API

**Opción A - Usando el script (Recomendado):**
```bash
cd backend
iniciar_api.bat
```

**Opción B - Manualmente:**
```bash
cd backend
python api_scouting_fifa.py
```

**IMPORTANTE:** La primera carga puede tardar 30-60 segundos (carga modelo de 2000 árboles + dataset de 122K jugadores)

### 2. Verificar que está funcionando

Abrir en el navegador: **http://localhost:8000**

Deberías ver un JSON con información de la API.

### 3. Acceder a la Documentación Interactiva

Abrir en el navegador: **http://localhost:8000/docs**

Aquí puedes probar todos los endpoints directamente desde el navegador.

---

## Probar la API con Script

**En otra terminal** (mientras la API está corriendo):

```bash
cd backend
python probar_api.py
```

Este script ejecuta pruebas automáticas de todos los endpoints.

---

## Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información general de la API |
| `/docs` | GET | Documentación interactiva (Swagger UI) |
| `/jugadores/filtros` | GET | Opciones de filtros disponibles |
| `/jugadores/buscar` | GET | Buscar jugadores con filtros |
| `/jugadores/{id}/perfil` | GET | Perfil completo de un jugador |
| `/ml/predecir_valor` | POST | **Predecir valor de mercado** (ML) |
| `/jugadores/infravalorados` | GET | Top jugadores infravalorados |
| `/jugadores/sobrevalorados` | GET | Top jugadores sobrevalorados |
| `/eda/estadisticas_generales` | GET | KPIs del dataset |
| `/eda/datos_graficos` | GET | Datos para visualizaciones |

---

## Ejemplos de Uso

### Ejemplo 1: Buscar los 10 jugadores más valiosos

**URL:** http://localhost:8000/jugadores/buscar?limite=10&ordenar_por=valor_mercado_eur&orden_descendente=true

### Ejemplo 2: Buscar delanteros jóvenes prometedores

**URL:** http://localhost:8000/jugadores/buscar?categoria_posicion=Delantero&edad_min=18&edad_max=23&potencial_min=80&limite=20

### Ejemplo 3: Ver perfil de un jugador

**URL:** http://localhost:8000/jugadores/158023/perfil

(Reemplazar `158023` con el ID del jugador que quieras ver)

### Ejemplo 4: Predecir valor de un jugador (POST)

Ir a http://localhost:8000/docs y usar el endpoint `/ml/predecir_valor`

O usando Python:

```python
import requests

url = "http://localhost:8000/ml/predecir_valor"
datos = {
    "edad": 22,
    "valoracion_global": 78,
    "potencial": 85,
    "ritmo_velocidad": 88,
    "tiro_disparo": 72,
    "pase": 70,
    "posiciones_jugador": "LW",
    "nacionalidad": "Argentina"
}

response = requests.post(url, json=datos)
print(response.json())
```

### Ejemplo 5: Ver jugadores infravalorados

**URL:** http://localhost:8000/jugadores/infravalorados?top=20&diferencia_minima_porcentual=30&edad_maxima=25

---

## Características del Modelo ML

- **Tipo:** Random Forest Regressor
- **R² Score:** 98.30% (precisión excepcional)
- **Features:** 110 (48 numéricas + 62 categóricas)
- **Jugadores entrenamiento:** 91,875
- **Error promedio:** €333,865 (13.2% relativo)

---

## Solución de Problemas

### La API no inicia

1. Verificar que estás en el directorio `backend`
2. Verificar que el entorno virtual está activado
3. Verificar que existen los archivos en `backend/models/`:
   - `modelo_fifa.joblib`
   - `encoder_fifa.joblib`
   - `club_encoding_fifa.joblib`

### Error "ModuleNotFoundError"

Instalar dependencias:
```bash
pip install -r requirements-api.txt
```

### La API tarda mucho en cargar

Es normal. El modelo tiene 2000 árboles y el dataset 122K jugadores. Espera 30-60 segundos.

### Puerto 8000 ya en uso

Matar el proceso:
```powershell
Get-Process python | Where-Object {$_.Path -like '*python*'} | Stop-Process -Force
```

Luego reiniciar la API.

---

## Documentación Completa

Ver: `documentacion/api_documentacion_completa.md`

---

## Estado del Proyecto

✅ **FASE 5 COMPLETADA: API REST**

**Próximo paso:** FASE 6 - Dashboard interactivo con Streamlit
