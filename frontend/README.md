# 📊 FRONTEND - Dashboard Scouting FIFA

Dashboard interactivo con Streamlit para visualización, análisis y predicción del valor de mercado de jugadores de fútbol.

---

## 📁 Estructura del Frontend

```
frontend/
│
├── 📄 dashboard_scouting_fifa.py      # Dashboard principal Streamlit
├── 📄 requirements-dashboard.txt      # Dependencias del dashboard
└── 📄 README.md                       # Este archivo
```

---

## 🎨 Características del Dashboard

### 🔍 **TAB 1: Exploración de Jugadores**

**Funcionalidades:**
- 🔎 Búsqueda avanzada con múltiples filtros
- 📋 Tabla interactiva de resultados
- 🃏 Ficha detallada de jugador
- 📈 Gráfico radar con 6 atributos clave
- 💰 Información de valor de mercado y salario

**Filtros disponibles:**
- Posición (27 posiciones únicas)
- Club (954 clubes)
- Liga (39 ligas)
- Nacionalidad (164 países)
- Rango de edad
- Valoración global (overall)
- Potencial
- Valor de mercado
- Pie preferido

---

### 📊 **TAB 2: Análisis de Mercado**

**Visualizaciones:**
- 📊 Top 20 jugadores más valiosos
- 🏆 Top 20 clubes con mayor valor total de plantilla
- 🌍 Top 20 ligas más valiosas
- 🎯 Análisis de distribución por posición
- 💎 Jugadores infravalorados (oportunidades)
- 💸 Jugadores sobrevalorados

**Métricas generales:**
- Total de jugadores en base de datos
- Valor promedio de mercado
- Edad promedio
- Overall promedio
- Distribución por categorías

---

### 🤖 **TAB 3: Predicción de Valor**

**Funcionalidades:**
- 📝 Formulario interactivo con atributos del jugador
- 🔮 Predicción en tiempo real usando Random Forest
- 💡 Nivel de confianza de la predicción
- 📊 Comparación con jugadores similares
- 🎯 Recomendaciones basadas en el valor predicho

**Atributos requeridos:**
- Información básica (edad, posición, nacionalidad)
- Atributos técnicos (overall, potencial, ritmo, tiro, pase, etc.)
- Información del club (club, liga)
- Atributos físicos (altura, peso)
- Características adicionales (pie preferido, reputación)

---

## 🚀 Ejecución del Dashboard

### **Opción 1: Ejecución Local (desarrollo)**

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ir a carpeta frontend
cd frontend

# Instalar dependencias
pip install -r requirements-dashboard.txt

# Iniciar dashboard
streamlit run dashboard_scouting_fifa.py
```

**🌐 Dashboard disponible en:** http://localhost:8501

**⚠️ Requisito previo:** La API debe estar corriendo en http://localhost:8000

---

### **Opción 2: Ejecución en Docker (producción)**

El dashboard está diseñado para ejecutarse en un **contenedor Docker** junto con la API REST.

#### Configuración Docker:

```yaml
# docker-compose.yml
services:
  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://backend:8000
    depends_on:
      - backend
    volumes:
      - ../datos:/app/datos
```

#### Variables de entorno:

| Variable | Valor Local | Valor Docker |
|----------|-------------|--------------|
| `API_BASE_URL` | `http://localhost:8000` | `http://backend:8000` |

El dashboard detecta automáticamente si está en Docker usando `os.getenv("API_BASE_URL")`.

---

## 🐳 Despliegue con Docker

### Iniciar servicios completos (API + Dashboard):

```powershell
# Ir a carpeta docker
cd docker

# Levantar servicios
docker-compose up --build

# O en segundo plano
docker-compose up -d --build
```

**🌐 Servicios disponibles:**
- **Dashboard:** http://localhost:8501
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Detener servicios:

```powershell
docker-compose down

# Con limpieza de volúmenes
docker-compose down -v
```

---

## 🎨 Diseño y Estilo

### Paleta de colores:

```python
COLOR_PRIMARIO = "#000000"      # Negro
COLOR_SECUNDARIO = "#7890a8"    # Azul grisáceo
COLOR_ACENTO_1 = "#304878"      # Azul oscuro
COLOR_ACENTO_2 = "#181848"      # Azul muy oscuro
COLOR_DESTACADO = "#f0a818"     # Dorado/Naranja
```

### Componentes personalizados:

- 🃏 **Fichas de jugadores** estilo tarjeta FIFA
- 📊 **Gráficos radar** con Plotly (atributos técnicos)
- 📈 **Tablas interactivas** con filtrado y ordenamiento
- 🎯 **Métricas destacadas** con diseño card
- 🌈 **Barras de progreso** para atributos

---

## 📊 Gráficos y Visualizaciones

### Tipos de gráficos disponibles:

1. **Gráfico Radar** (atributos de jugador)
   - Ritmo
   - Tiro
   - Pase
   - Regate
   - Defensa
   - Físico

2. **Gráficos de Barras**
   - Top jugadores por valor
   - Top clubes por valor
   - Top ligas por valor

3. **Histogramas**
   - Distribución de edades
   - Distribución de overall
   - Distribución de valores de mercado

4. **Scatter Plots**
   - Overall vs Valor de mercado
   - Potencial vs Valor de mercado
   - Edad vs Valor de mercado

---

## 🔌 Integración con la API

### Endpoints utilizados:

| Endpoint | Uso en Dashboard |
|----------|------------------|
| `GET /jugadores/filtros` | Cargar opciones de filtros |
| `GET /jugadores/buscar` | Búsqueda de jugadores |
| `GET /jugadores/{id}/perfil` | Ficha de jugador |
| `POST /ml/predecir_valor` | Predicción ML |
| `GET /jugadores/infravalorados` | Top oportunidades |
| `GET /jugadores/sobrevalorados` | Jugadores caros |
| `GET /eda/estadisticas_generales` | KPIs generales |
| `GET /eda/datos_graficos` | Datos para visualizaciones |

### Manejo de errores:

```python
# Sesión HTTP con reintentos automáticos
sesion = requests.Session()
reintentos = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
```

- ✅ Reintentos automáticos (máximo 5)
- ✅ Mensajes de error amigables
- ✅ Indicadores de carga (spinners)
- ✅ Timeouts configurados

---

## 📦 Dependencias

### requirements-dashboard.txt:

```txt
streamlit>=1.28.0
plotly>=5.17.0
requests>=2.31.0
pandas>=2.1.0
```

### Versiones instaladas actualmente:

```txt
streamlit==1.50.0
plotly==6.4.0
requests==2.32.5
pandas==2.3.3
```

---

## 🛠️ Solución de Problemas

### ❌ Error "Connection refused" al buscar jugadores

**Causa:** La API no está corriendo

**Solución:**
```powershell
# Iniciar API primero
cd backend
python api_scouting_fifa.py
```

---

### ❌ Dashboard se ve mal o sin estilos

**Causa:** CSS no se cargó correctamente

**Solución:**
```powershell
# Limpiar caché de Streamlit
streamlit cache clear

# Reiniciar dashboard
streamlit run dashboard_scouting_fifa.py
```

---

### ❌ Error al cargar datos de gráficos

**Causa:** Endpoint de API no responde

**Solución:**
1. Verificar que la API está corriendo
2. Verificar que el dataset existe en `datos/procesados/fifa_limpio.csv`
3. Revisar logs de la API

---

### ⏳ Dashboard tarda mucho en cargar

**Causa:** Primera carga de datos desde la API

**Es normal:**
- Primera carga: 5-10 segundos
- Cargas siguientes: < 1 segundo (caché)

**Optimización:**
```python
@st.cache_data
def cargar_opciones_filtros():
    # Streamlit cachea automáticamente
```

---

### ❌ Puerto 8501 ya en uso

**Solución:**
```powershell
# Usar otro puerto
streamlit run dashboard_scouting_fifa.py --server.port 8502
```

---

## 🎯 Características Técnicas

### Performance:

- ✅ **Caché inteligente** de datos con `@st.cache_data`
- ✅ **Lazy loading** de gráficos pesados
- ✅ **Paginación** en tablas grandes
- ✅ **Conexión HTTP persistente** con reintentos

### Responsividad:

- ✅ Layout adaptable (`layout="wide"`)
- ✅ Columnas responsive
- ✅ Sidebar colapsable
- ✅ Gráficos escalables

### Accesibilidad:

- ✅ Colores de alto contraste
- ✅ Tooltips informativos
- ✅ Mensajes de error claros
- ✅ Feedback visual de acciones

---

## 🚀 Próximas Mejoras

### Pendientes:

- [ ] Exportar resultados de búsqueda a CSV/Excel
- [ ] Comparación lado a lado de jugadores
- [ ] Histórico de predicciones
- [ ] Guardado de filtros favoritos
- [ ] Modo oscuro/claro
- [ ] Traducción multi-idioma

### En desarrollo:

- [ ] Autenticación de usuarios
- [ ] Dashboard personalizado por usuario
- [ ] Alertas de oportunidades en tiempo real

---

## 📚 Documentación de Usuario

### Para scouts deportivos:

1. **Buscar jugadores infravalorados:**
   - Tab 2 → Sección "💎 Oportunidades de Mercado"
   - Filtrar por edad, posición y diferencia % mínima

2. **Analizar atributos de un jugador:**
   - Tab 1 → Buscar jugador → Ver ficha
   - Revisar gráfico radar de atributos

3. **Predecir valor de un prospecto:**
   - Tab 3 → Completar formulario
   - Obtener predicción con nivel de confianza

---

## 🔐 Seguridad

### Variables de entorno:

```bash
# .env (no incluir en git)
API_BASE_URL=http://localhost:8000
```

### Validación de datos:

- ✅ Validación de formularios en cliente
- ✅ Sanitización de inputs
- ✅ Timeouts en peticiones HTTP
- ✅ Manejo seguro de errores

---

## 📊 Métricas y Analytics

### Estadísticas del dashboard:

- Total de jugadores: 122,501
- Países representados: 164
- Clubes: 954
- Ligas: 39
- Posiciones: 27

---

## 👨‍💻 Uso Interno

Este README está orientado a desarrolladores del frontend.

**Para documentación completa del proyecto:**
- Ver: `README.md` (raíz del proyecto)
- Ver: `backend/README.md` (documentación del backend)
- Ver: `docker/README.md` (documentación de Docker)

---

## 🎓 Créditos

**Proyecto:** Sistema de Scouting y Valoración FIFA  
**Asignatura:** Seminario Complexivo de Titulación - Analítica con Python  
**Institución:** Universidad Regional Autónoma de los Andes (UniAndes)  
**Profesor:** Juan Felipe Nájera  
**Fecha:** Noviembre 2025

---

**⚽ Dashboard listo para explorar y analizar jugadores de fútbol profesional! 🚀**
