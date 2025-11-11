# Cambios de Configuración - Dashboard Frontend

## Problema Identificado

Al ejecutar el dashboard dentro del contenedor Docker, se presentaba el siguiente error:

```
Error al buscar jugadores: HTTPConnectionPool(host='localhost', port=8000): 
Max retries exceeded with url: /jugadores/buscar
Connection refused
```

## Causa del Problema

El dashboard estaba configurado con:
```python
API_BASE_URL = "http://localhost:8000"
```

Cuando se ejecuta dentro de un contenedor Docker, `localhost` se refiere al **mismo contenedor** (frontend), no al contenedor del backend. Por lo tanto, la conexión fallaba porque no había ningún servicio escuchando en el puerto 8000 dentro del contenedor del frontend.

## Solución Implementada

Se modificó el archivo `frontend/dashboard_scouting_fifa.py` para usar una variable de entorno:

```python
import os

# Si está en Docker, usa la variable de entorno API_BASE_URL
# Si está en desarrollo local, usa localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

### Configuración en docker-compose.yml

El archivo `docker-compose.yml` ya tenía configurada la variable de entorno:

```yaml
frontend:
  environment:
    - TZ=America/Guayaquil
    - LANG=C.UTF-8
    - LC_ALL=C.UTF-8
    - PYTHONIOENCODING=utf-8
    - API_BASE_URL=http://backend:8000  # ← Usa el nombre del servicio
```

## Comunicación entre Contenedores

En Docker Compose, los contenedores pueden comunicarse usando los nombres de los servicios como hostnames. En nuestro caso:

- **Backend service name**: `backend`
- **Frontend service name**: `frontend`
- **Network**: `fifa-network` (bridge)

Por lo tanto, el frontend puede acceder al backend usando `http://backend:8000` en lugar de `http://localhost:8000`.

## Funcionamiento

### En Docker
- **API_BASE_URL**: `http://backend:8000` (tomado de variable de entorno)
- **Conectividad**: Frontend → Backend a través de red Docker

### En Desarrollo Local
- **API_BASE_URL**: `http://localhost:8000` (valor por defecto)
- **Conectividad**: Frontend → Backend a través de localhost

## Verificación

Para verificar que la configuración es correcta:

```bash
# Ver variable de entorno en el contenedor
docker exec fifa-frontend printenv API_BASE_URL

# Probar conectividad desde frontend a backend
docker exec fifa-frontend python -c "import requests; print(requests.get('http://backend:8000/').json())"
```

## Resultado

✅ El dashboard ahora puede comunicarse correctamente con el backend dentro de Docker
✅ Mantiene compatibilidad con desarrollo local
✅ No requiere cambios manuales al cambiar entre Docker y desarrollo local

---

**Fecha de Actualización**: 9 de noviembre de 2025
