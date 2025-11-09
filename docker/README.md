# 🐳 Docker - Sistema de Scouting FIFA# 🐳 Docker - Sistema de Scouting FIFA



Contenedorización completa del sistema de scouting inteligente FIFA con backend (FastAPI) y frontend (Streamlit).Contenedorización completa del sistema de scouting inteligente FIFA con backend (FastAPI) y frontend (Streamlit).



------



## 📁 Estructura de Archivos## 📁 Estructura de Archivos



``````

docker/docker/

││

├── 📄 Dockerfile.backend          # Imagen para API (FastAPI)├── 📄 Dockerfile.backend          # Imagen para API (FastAPI)

├── 📄 Dockerfile.frontend         # Imagen para Dashboard (Streamlit)├── 📄 Dockerfile.frontend         # Imagen para Dashboard (Streamlit)

├── 📄 docker-compose.yml          # Orquestación de servicios├── 📄 docker-compose.yml          # Orquestación de servicios

└── 📄 README.md                   # Este archivo└── 📄 README.md                   # Este archivo

``````



**Nota:** El `.dockerignore` está en la **raíz del proyecto**, no aquí.**Nota:** El `.dockerignore` está en la raíz del proyecto, no aquí.



------



## 🐳 Arquitectura de Contenedores## � Arquitectura de Contenedores



### Servicios:### Servicios:



| Servicio | Contenedor | Puerto | Descripción || Servicio | Imagen | Puerto | Descripción |

|----------|------------|--------|-------------||----------|--------|--------|-------------|

| **backend** | `fifa-backend` | 8000 | API REST (FastAPI + Random Forest) || **backend** | `fifa-backend` | 8000 | API REST (FastAPI) |

| **frontend** | `fifa-frontend` | 8501 | Dashboard (Streamlit) || **frontend** | `fifa-frontend` | 8501 | Dashboard (Streamlit) |



### Red:### Red:



- **fifa-network** (bridge): Red interna para comunicación entre contenedores- **fifa-network** (bridge): Red interna para comunicación entre contenedores

  - Frontend → Backend: `http://backend:8000`

### Volúmenes:

### Volúmenes:

- `../datos:/app/datos:ro` - Datos montados en modo **read-only** con persistencia (no modificables desde contenedores)

```yaml

volumes:---

  - ../datos:/app/datos:ro  # Montaje read-only (no modificable desde contenedores)

```## 🛠️ Características Técnicas



**Contenido montado:**### Ambas imágenes:

- `datos/procesados/fifa_limpio.csv` (122,501 jugadores)

- `datos/modelos/*.joblib` (3 archivos: modelo, encoder, club_encoding)- ✅ **Python 3.11-slim** (imagen base ligera)

- ✅ **Zona horaria:** America/Guayaquil (Ecuador)

---- ✅ **Codificación:** UTF-8 (soporte para tildes y ñ)

- ✅ **Variables de entorno:** LANG, LC_ALL, PYTHONIOENCODING

## 🛠️ Características Técnicas- ✅ **Optimizadas:** Sin caché de pip, sin archivos innecesarios



### Ambas imágenes:### Backend específico:



| Característica | Valor |- ✅ **Librería libgomp1** instalada (requerida por LightGBM/scikit-learn)

|----------------|-------|- ✅ **Health check** configurado (verifica que la API responda)

| **Imagen base** | python:3.11-slim |- ✅ **Start period** de 40 segundos (tiempo para cargar modelo de 4000 árboles)

| **Zona horaria** | America/Guayaquil (Ecuador) |

| **Codificación** | UTF-8 (LANG, LC_ALL, PYTHONIOENCODING) |### Frontend específico:

| **Optimización** | `--no-cache-dir` en pip |

| **Tamaño** | ~300-400 MB (backend), ~200-300 MB (frontend) |- ✅ **Depende de backend** (espera health check)

- ✅ **Variable API_BASE_URL** configurada automáticamente

### Backend (Dockerfile.backend):- ✅ **Streamlit** en modo servidor (accesible desde cualquier IP)



```dockerfile---

FROM python:3.11-slim

## 🚀 Uso

# Zona horaria y UTF-8

ENV TZ=America/Guayaquil### Opción 1: Docker Compose (Recomendado)

ENV LANG=C.UTF-8

ENV LC_ALL=C.UTF-8## Requisitos Previos



# Instalar libgomp1 (requerido por scikit-learn/LightGBM)Levanta ambos servicios en la misma red:

RUN apt-get update && apt-get install -y libgomp1

- Docker Desktop instalado y ejecutándose

# Copiar código

COPY backend/*.py ./backend/- Docker Compose instalado (incluido con Docker Desktop)```powershell

COPY backend/scripts/ ./backend/scripts/

# Desde la carpeta docker/

# Crear carpetas para volúmenes

RUN mkdir -p /app/datos/modelos## Construcción y Ejecucióncd docker



# Exponer puerto

EXPOSE 8000

### Opción 1: Usando Docker Compose (Recomendado)# Construir y levantar servicios

# Comando de inicio

CMD ["uvicorn", "backend.api_scouting_fifa:app", "--host", "0.0.0.0", "--port", "8000"]docker-compose up --build

```

```bash

**Health check:**

- Intervalo: 10 segundos# Desde el directorio raíz del proyecto# En segundo plano (detached)

- Timeout: 5 segundos

- Reintentos: 5cd dockerdocker-compose up -d --build

- Start period: 40 segundos (tiempo para cargar modelo de 4000 árboles)



### Frontend (Dockerfile.frontend):

# Construir y ejecutar ambos contenedores# Ver logs

```dockerfile

FROM python:3.11-slimdocker-compose up --builddocker-compose logs -f



# Zona horaria y UTF-8

ENV TZ=America/Guayaquil

ENV LANG=C.UTF-8# O en modo detached (segundo plano)# Detener servicios



# Copiar códigodocker-compose up --build -ddocker-compose down

COPY frontend/ ./frontend/

``````

# Exponer puerto

EXPOSE 8501



# Comando de inicio### Opción 2: Construcción Manual### Opción 2: Construir Imágenes Individuales

CMD ["streamlit", "run", "frontend/dashboard_scouting_fifa.py", \

     "--server.port=8501", "--server.address=0.0.0.0"]

```

```bash```powershell

**Dependencias:**

- Espera a que backend esté `healthy` antes de iniciar# Construir backend# Backend

- Variable de entorno `API_BASE_URL=http://backend:8000`

docker build -f docker/Dockerfile.backend -t fifa-backend:latest .docker build -f docker/Dockerfile.backend -t fifa-backend .

---



## 🚀 Uso

# Construir frontend# Frontend

### ⚠️ Requisitos Previos

docker build -f docker/Dockerfile.frontend -t fifa-frontend:latest .docker build -f docker/Dockerfile.frontend -t fifa-frontend .

**Antes de levantar Docker, asegúrate de tener:**



1. ✅ **Docker Desktop** instalado y ejecutándose

2. ✅ **Datos procesados:** `datos/procesados/fifa_limpio.csv` (122,501 jugadores)# Crear red# Ejecutar contenedores

3. ✅ **Modelos entrenados** en `datos/modelos/`:

   - `modelo_fifa.joblib` (500-800 MB)docker network create fifa-networkdocker run -d -p 8000:8000 --name backend fifa-backend

   - `encoder_fifa.joblib` (5-10 MB)

   - `club_encoding_fifa.joblib` (100-200 KB)docker run -d -p 8501:8501 --name frontend fifa-frontend



**Si NO tienes los datos/modelos:**# Ejecutar backend```



```powershelldocker run -d --name fifa-backend --network fifa-network -p 8000:8000 fifa-backend:latest

# Activar entorno virtual

.\venv\Scripts\Activate.ps1---



# 1. Ejecutar pipeline de limpieza# Ejecutar frontend

cd backend

python pipeline_limpieza_datos.pydocker run -d --name fifa-frontend --network fifa-network -p 8501:8501 -e API_BASE_URL=http://backend:8000 fifa-frontend:latest## 🌐 Acceso a Servicios



# 2. Entrenar modelos ML (tarda 10-15 minutos)```

python entrenamiento.py

Una vez levantados los contenedores:

# Verificar que se crearon los archivos

ls ..\datos\procesados## Acceso a los Servicios

ls ..\datos\modelos

```- **API Backend**: http://localhost:8000



---Una vez ejecutándose:- **API Docs (Swagger)**: http://localhost:8000/docs



### 🚀 Opción 1: Docker Compose (Recomendado)- **Dashboard Frontend**: http://localhost:8501



Levanta ambos servicios (backend + frontend) con un solo comando:- **API Backend**: http://localhost:8000



```powershell- **API Documentación**: http://localhost:8000/docs---

# Ir a carpeta docker

cd docker- **Dashboard Frontend**: http://localhost:8501



# Construir y levantar servicios## 🔗 Red de Comunicación

docker-compose up --build

## Comandos Útiles

# O en segundo plano (detached mode)

docker-compose up -d --buildLos servicios están en la misma red Docker (`fifa_network`):

```

```bash

**Ver logs:**

# Ver logs- El frontend se comunica con el backend mediante `http://backend:8000`

```powershell

# Logs de ambos serviciosdocker-compose logs -f- El backend expone el puerto 8000

docker-compose logs -f

- El frontend expone el puerto 8501

# Logs solo del backend

docker-compose logs -f backend# Ver logs de un servicio específico



# Logs solo del frontenddocker-compose logs -f backend---

docker-compose logs -f frontend

```docker-compose logs -f frontend



**Detener servicios:**## 📝 Notas Importantes



```powershell# Detener contenedores

# Detener contenedores

docker-compose downdocker-compose down### Antes de levantar Docker:



# Detener y eliminar volúmenes (NO recomendado, perderías datos)

docker-compose down -v

```# Detener y eliminar volúmenes1. **Ejecutar pipeline de limpieza**:



**Reiniciar un servicio:**docker-compose down -v   ```powershell



```powershell   python backend/main.py

# Reiniciar backend

docker-compose restart backend# Reiniciar servicios   ```



# Reiniciar frontenddocker-compose restart   Esto genera `datos/fifa_limpio.csv`

docker-compose restart frontend

```



---# Ver contenedores en ejecución2. **Entrenar modelo ML**:



### 🔧 Opción 2: Construcción Manual (Avanzado)docker-compose ps   ```powershell



Si prefieres controlar cada contenedor individualmente:   python backend/train.py



#### 1. Construir imágenes:# Acceder a terminal de un contenedor   ```



```powershelldocker-compose exec backend bash   Esto genera los modelos en `backend/models/`

# Desde la raíz del proyecto (importante: context=raíz)

docker-compose exec frontend bash

# Backend

docker build -f docker/Dockerfile.backend -t fifa-backend .```3. **Verificar que existan**:



# Frontend   - `datos/fifa_limpio.csv`

docker build -f docker/Dockerfile.frontend -t fifa-frontend .

```## Verificación de Funcionamiento   - `backend/models/modelo_fifa.joblib`



#### 2. Crear red:   - `backend/models/encoder_fifa.joblib`



```powershell1. **Backend API**:

docker network create fifa-network

```   ```bash### Volúmenes montados:



#### 3. Ejecutar backend:   curl http://localhost:8000/



```powershell   ```- `datos/` - Permite acceso a los datasets

docker run -d `

  --name fifa-backend `- `backend/models/` - Permite acceso a modelos entrenados

  --network fifa-network `

  -p 8000:8000 `2. **Frontend Dashboard**:

  -v "${PWD}/datos:/app/datos:ro" `

  -e TZ=America/Guayaquil `   Abrir navegador en http://localhost:8501---

  fifa-backend

```



#### 4. Ejecutar frontend:3. **Conectividad entre contenedores**:## 🛠️ Comandos Útiles



```powershell   El frontend debe poder comunicarse con el backend a través de la red `fifa-network`

docker run -d `

  --name fifa-frontend ````powershell

  --network fifa-network `

  -p 8501:8501 `## Troubleshooting# Ver contenedores activos

  -e API_BASE_URL=http://backend:8000 `

  -e TZ=America/Guayaquil `docker ps

  fifa-frontend

```### Puerto en uso



#### 5. Limpiar:Si algún puerto está ocupado:# Ver logs de un servicio específico



```powershell```bashdocker-compose logs backend

# Detener y eliminar contenedores

docker stop fifa-backend fifa-frontend# Windowsdocker-compose logs frontend

docker rm fifa-backend fifa-frontend

netstat -ano | findstr :8000

# Eliminar red

docker network rm fifa-networknetstat -ano | findstr :8501# Reiniciar un servicio



# Eliminar imágenesdocker-compose restart backend

docker rmi fifa-backend fifa-frontend

```# Detener proceso



---taskkill /PID <PID> /F# Eliminar contenedores y red



## 🌐 Acceso a Servicios```docker-compose down



Una vez levantados los contenedores:



| Servicio | URL | Descripción |### Reconstruir sin caché# Eliminar también volúmenes

|----------|-----|-------------|

| **API Backend** | http://localhost:8000 | Endpoint raíz (health check) |```bashdocker-compose down -v

| **API Docs** | http://localhost:8000/docs | Documentación interactiva Swagger |

| **Dashboard** | http://localhost:8501 | Interfaz Streamlit |docker-compose build --no-cache



### Verificar funcionamiento:docker-compose up# Reconstruir sin caché



```powershell```docker-compose build --no-cache

# Test API (debe retornar JSON)

curl http://localhost:8000```



# Test Dashboard (debe abrir navegador)### Limpiar todo Docker

start http://localhost:8501

``````bash---



---docker-compose down



## 🔗 Comunicación entre Contenedoresdocker system prune -a## 🐛 Troubleshooting



### Diagrama de red:```



```### Frontend no se conecta al backend:

┌─────────────────┐

│   Host Machine  │## Notas Importantes

│   (tu PC)       │

└────────┬────────┘Verifica que el `API_URL` en `docker-compose.yml` apunte a:

         │

    ┌────┴──────┐1. El archivo `fifa_limpio.csv` debe estar en `datos/` antes de construir```yaml

    │  Docker   │

    │  Network  │2. Los modelos ML deben estar en `backend/models/`API_URL=http://backend:8000

    └─┬───────┬─┘

      │       │3. La primera construcción puede tardar varios minutos```

┌─────┴──┐ ┌──┴──────┐

│Backend │ │Frontend │4. El backend carga 122,501 jugadores y modelos de ~5GB

│:8000   │←│:8501    │

└────────┘ └─────────┘Y en `frontend/dashboard_app.py` usa la variable de entorno:

```

## Configuración UTF-8```python

- **Frontend → Backend:** `http://backend:8000` (red interna)

- **Host → Backend:** `http://localhost:8000` (puerto expuesto)import os

- **Host → Frontend:** `http://localhost:8501` (puerto expuesto)

Los contenedores están configurados con:API_URL = os.getenv("API_URL", "http://localhost:8000")

---

- `LANG=C.UTF-8````

## 📊 Tiempos de Carga

- `LC_ALL=C.UTF-8`

| Fase | Tiempo estimado | Descripción |

|------|-----------------|-------------|- `PYTHONIOENCODING=utf-8`### Error al construir imágenes:

| **Construcción** | 3-5 minutos | Primera vez (descarga Python 3.11 + dependencias) |

| **Reconstrucción** | 1-2 minutos | Con caché de Docker |- Zona horaria: `America/Guayaquil`

| **Inicio Backend** | 30-60 segundos | Carga modelo (4000 árboles) + dataset (122K) |

| **Inicio Frontend** | 5-10 segundos | Streamlit + conexión a backend |Asegúrate de ejecutar los comandos desde la **raíz del proyecto**, no desde `docker/`.



---Esto garantiza correcto manejo de:



## 🛠️ Comandos Útiles- Tildes (á, é, í, ó, ú)### Modelo no cargado:



### Ver estado de contenedores:- Letra ñ



```powershell- Caracteres especiales latinosVerifica que los modelos estén entrenados y guardados en `backend/models/` antes de construir las imágenes.

# Con docker-compose

docker-compose ps



# Con docker nativo## Producción---

docker ps

docker ps -a  # Incluye detenidos

```

Para desplegar en producción, considerar:## ✅ Checklist Pre-Deploy

### Inspeccionar contenedor:



```powershell

# Ver configuración completa1. **Variables de entorno**: Usar `.env` para configuración- [ ] Pipeline ejecutado (`datos/fifa_limpio.csv` existe)

docker inspect fifa-backend

2. **Volúmenes**: Persistir datos si es necesario- [ ] Modelo entrenado (`backend/models/*.joblib` existen)

# Ver solo IP interna

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' fifa-backend3. **Health checks**: Agregar verificaciones de salud- [ ] Docker instalado y corriendo

```

4. **Escalado**: Usar réplicas con Docker Swarm o Kubernetes- [ ] Puertos 8000 y 8501 libres

### Acceder a terminal dentro del contenedor:

5. **Reverse proxy**: Nginx o Traefik para SSL/TLS- [ ] Archivos Dockerfile revisados

```powershell

# Backend- [ ] docker-compose.yml configurado

docker-compose exec backend bash

## Autor

# Frontend

docker-compose exec frontend bash---



# Ejemplo: verificar archivos montadosSeminario Complexivo de Titulación - Uniandes

docker-compose exec backend ls -lh /app/datos/modelos

```


### Ver uso de recursos:

```powershell
# Uso de CPU, RAM, red, disco
docker stats

# Solo backend
docker stats fifa-backend
```

---

## 🐛 Troubleshooting

### ❌ Error: "Port 8000 is already allocated"

**Causa:** El puerto ya está siendo usado por otro proceso.

**Solución:**

```powershell
# Encontrar proceso usando el puerto
netstat -ano | findstr :8000

# Matar proceso (reemplaza <PID> con el número)
taskkill /PID <PID> /F

# O cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usa 8001 en el host
```

---

### ❌ Frontend no se conecta a backend

**Síntomas:** Dashboard muestra "Connection refused"

**Solución:**

1. Verificar que backend esté healthy:
```powershell
docker-compose ps
# Estado debe ser "healthy", no "unhealthy"
```

2. Verificar logs de backend:
```powershell
docker-compose logs backend
```

3. Verificar variable de entorno en frontend:
```powershell
docker-compose exec frontend env | grep API_BASE_URL
# Debe mostrar: API_BASE_URL=http://backend:8000
```

---

### ❌ Error: "FileNotFoundError: modelo_fifa.joblib"

**Causa:** Los modelos no existen en `datos/modelos/`.

**Solución:**

```powershell
# Entrenar modelos ANTES de levantar Docker
.\venv\Scripts\Activate.ps1
cd backend
python entrenamiento.py

# Verificar que se crearon
ls ..\datos\modelos
# Debe listar: modelo_fifa.joblib, encoder_fifa.joblib, club_encoding_fifa.joblib
```

---

### ❌ Backend tarda mucho en estar "healthy"

**Causa:** Normal. El modelo tiene 4000 árboles y carga 122K jugadores.

**Tiempos esperados:**
- Start period: 40 segundos (configurado en docker-compose.yml)
- Carga completa: 30-60 segundos

**Ver progreso:**
```powershell
docker-compose logs -f backend
# Busca: "✓ TODOS LOS COMPONENTES CARGADOS EXITOSAMENTE"
```

---

### ❌ Error: "Cannot find module 'backend'"

**Causa:** Estructura de archivos incorrecta o WORKDIR mal configurado.

**Solución:**

Verificar que los Dockerfiles copien correctamente:
```dockerfile
# Debe ser así:
COPY backend/*.py ./backend/
COPY backend/scripts/ ./backend/scripts/
```

---

### ⏳ Reconstruir sin caché

Si hay problemas persistentes, forzar reconstrucción completa:

```powershell
# Detener todo
docker-compose down

# Limpiar caché de Docker
docker-compose build --no-cache

# Levantar de nuevo
docker-compose up -d
```

---

### 🧹 Limpiar Docker completamente

Si necesitas empezar de cero:

```powershell
# Detener contenedores del proyecto
docker-compose down -v

# Eliminar todas las imágenes del proyecto
docker rmi fifa-backend fifa-frontend

# (Opcional) Limpiar todo Docker (cuidado: afecta otros proyectos)
docker system prune -a
```

---

## 📝 Notas Importantes

### ✅ Ventajas de usar volúmenes para datos:

- **No se reconstruyen** contenedores al actualizar datos
- **Persistencia** entre reinicios
- **Compartidos** entre backend y frontend
- **Imágenes ligeras** (sin incluir 1GB de datos)

### ⚠️ Volumen en modo read-only:

```yaml
volumes:
  - ../datos:/app/datos:ro  # :ro = read-only
```

**Razón:** Los contenedores no deben modificar datos originales. Si necesitas regenerar datos, hazlo en el host (con venv), no en Docker.

### 🔐 Seguridad:

- Los contenedores no tienen acceso root
- Red aislada (bridge, no host)
- Datos montados como read-only
- Sin contraseñas hardcodeadas

---

## 🚀 Despliegue en Producción

### Recomendaciones:

1. **Usar variables de entorno:**
   ```yaml
   environment:
     - API_KEY=${API_KEY}
     - DATABASE_URL=${DATABASE_URL}
   ```

2. **Agregar reverse proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       location / {
           proxy_pass http://localhost:8501;
       }
       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

3. **Usar Docker Swarm o Kubernetes** para escalado

4. **Configurar SSL/TLS** con Let's Encrypt

5. **Monitoreo** con Prometheus + Grafana

---

## 📚 Documentación Relacionada

- **Backend:** Ver `backend/README.md`
- **Frontend:** Ver `frontend/README.md`
- **Datos:** Ver `datos/README.md`
- **Proyecto completo:** Ver `README.md` (raíz)

---

## 🎓 Créditos

**Proyecto:** Sistema de Scouting y Valoración FIFA  
**Asignatura:** Seminario Complexivo - Analítica con Python  
**Institución:** Universidad Regional Autónoma de los Andes (UniAndes)  
**Profesor:** Juan Felipe Nájera  
**Fecha:** Noviembre 2025

---

**🐳 Sistema containerizado y listo para producción! ⚽🚀**
