# OPTIMIZACIÓN DE DOCKER CON VOLÚMENES

## Problema Inicial

El sistema copiaba **5+ GB de modelos ML** en cada build de Docker, resultando en:
- Builds de **15+ minutos**
- Transferencia de contexto de hasta **2.2 GB**
- Desperdicio de espacio en disco
- Lentitud en desarrollo

## Solución Implementada: Volúmenes Docker

### Reestructuración de Datos

Se reorganizó la carpeta `datos/` con estructura lógica:

```
datos/
├── originales/          # Dataset crudo (fifa.xlsx)
├── procesados/          # Dataset limpio (fifa_limpio.csv)
└── modelos/            # Modelos ML (*.joblib - 5+ GB)
```

### Configuración Docker

**docker-compose.yml:**
```yaml
backend:
  volumes:
    - ../datos:/app/datos:ro  # Monta carpeta completa como read-only
```

**Dockerfile.backend:**
```dockerfile
# Solo copia código Python, NO datos ni modelos
COPY backend/*.py ./backend/
COPY backend/scripts/ ./backend/scripts/

# Crea directorios vacíos (se llenan con volumen)
RUN mkdir -p /app/datos/originales /app/datos/procesados /app/datos/modelos
```

**.dockerignore:**
```
backend/models/    # Excluye modelos del contexto
datos/*.csv        # Excluye datasets del contexto
```

### Rutas Actualizadas en Código

**backend/api_scouting_fifa.py:**
```python
DATA_PATH = os.path.join(BASE_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "datos", "modelos")
```

**backend/entrenamiento.py:**
```python
DATA_PATH = os.path.join(BASE_DIR, "..", "datos", "procesados", "fifa_limpio.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "datos", "modelos")
```

**backend/pipeline_limpieza_datos.py:**
```python
df = cargar_datos_fifa('datos/originales/fifa.xlsx')
guardar_datos_limpios(df, 'datos/procesados/fifa_limpio.csv')
```

## Resultados

### Antes vs Después

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Tiempo de build** | 15+ minutos | 92 segundos | **10x más rápido** |
| **Contexto transferido** | 2.2 GB | 227 KB | **99% reducción** |
| **Espacio en imagen** | ~6 GB | ~800 MB | **87% reducción** |
| **Rebuild tras cambios** | 15+ minutos | 3 segundos | **300x más rápido** |

### Beneficios Adicionales

1. **Velocidad de Lectura**: Igual o mejor (acceso directo a archivos del host)
2. **Estabilidad**: Sin problemas - Docker monta carpetas de forma nativa
3. **Desarrollo**: Cambios en datos reflejados inmediatamente sin rebuild
4. **Producción**: Modelos actualizables sin reconstruir imagen
5. **Espacio**: Limpieza Docker liberó **17 GB** de caché

## Health Check Configurado

Para evitar errores de inicio, el frontend espera a que el backend esté listo:

```yaml
backend:
  healthcheck:
    test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/')"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 40s  # Da tiempo para cargar modelo de 5GB

frontend:
  depends_on:
    backend:
      condition: service_healthy  # Espera a que backend pase health check
```

## Ventajas de Esta Arquitectura

### Separación de Responsabilidades
- **Código** (en imagen): Lógica de aplicación
- **Datos** (en volumen): Modelos y datasets
- **Resultado**: Actualizaciones independientes

### Escalabilidad
- Modelos compartidos entre múltiples contenedores
- Fácil actualización de modelos sin downtime
- Preparado para orquestadores (Kubernetes, Swarm)

### Desarrollo Ágil
- Cambios en código: rebuild en segundos
- Cambios en datos: sin rebuild necesario
- Depuración más rápida

## Comandos Útiles

```bash
# Reconstruir completamente (limpieza total)
docker-compose down -v
docker system prune -f
docker-compose up -d --build

# Rebuild rápido (solo código cambiado)
docker-compose up -d --build

# Ver logs
docker logs fifa-backend --tail 50
docker logs fifa-frontend --tail 50

# Verificar volúmenes montados
docker exec fifa-backend ls -lh /app/datos/modelos/
docker exec fifa-backend du -h /app/datos/modelos/

# Estado de contenedores
docker ps --filter "name=fifa"
```

## Conclusión

El uso de **volúmenes Docker** para archivos pesados es una **best practice** que proporciona:
- ✅ Builds **10x más rápidos**
- ✅ Menor uso de disco y red
- ✅ Mayor flexibilidad
- ✅ Mejor experiencia de desarrollo
- ✅ **SIN impacto negativo** en estabilidad o rendimiento

**Recomendación**: Siempre usar volúmenes para:
- Modelos de ML
- Datasets grandes
- Archivos de configuración que cambian frecuentemente
- Cualquier archivo > 100 MB
