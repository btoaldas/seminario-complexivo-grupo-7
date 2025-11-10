# 🎓 Presentación Embebida en el Dashboard

## ✨ Nueva Funcionalidad Integrada

La presentación del proyecto de graduación ahora está **completamente integrada dentro del dashboard** de Streamlit, sin necesidad de abrir archivos externos.

---

## 🎯 Cómo Acceder a la Presentación

### Desde el Dashboard (http://localhost:8501)

1. **Abre el dashboard** en tu navegador: `http://localhost:8501`

2. **Localiza el botón** en la parte superior derecha:
   ```
   ┌─────────────────────────────────────────────────────┐
   │  ⚽ FIFA Scouting Pro - Dashboard ML   [🎓 Ver Presentación] │
   └─────────────────────────────────────────────────────┘
   ```

3. **Haz clic en "🎓 Ver Presentación"**

4. **Se abre un modal** con la presentación HTML completa embebida

5. **Navega dentro del modal**:
   - Usa **scroll** o **flechas ↓↑** para desplazarte entre secciones
   - Usa el **menú superior derecho** del HTML para saltos rápidos
   - Cada sección ocupa pantalla completa dentro del modal

6. **Cierra el modal** haciendo clic fuera de él o en la X

---

## 📊 Características

### ✅ Ventajas de la Integración

- **Sin salir del dashboard**: Todo en una sola aplicación
- **Acceso rápido**: Un solo clic para ver la presentación
- **Navegación fluida**: Scroll y menú integrados
- **Profesional**: Perfecto para demostraciones y defensa
- **Responsive**: Se adapta al tamaño del modal

### 🎨 Diseño del Modal

- **Ancho**: Grande (width='large') para mejor visualización
- **Altura**: 800px con scroll habilitado
- **Título**: "🎓 Presentación del Proyecto - Sistema de Scouting FIFA"
- **Instrucciones**: Incluidas en la parte superior del modal
- **Tip**: Opción de abrir en pantalla completa externa

---

## 🔧 Implementación Técnica

### Archivos Involucrados

```
frontend/
├── dashboard_scouting_fifa.py     # Dashboard principal con botón y modal
└── presentacion_defensa.html      # Presentación HTML (70KB)
```

### Código Clave

```python
# Botón en la parte superior
if st.button("🎓 Ver Presentación", use_container_width=True, type="primary"):
    st.session_state.mostrar_presentacion = True

# Modal con HTML embebido
@st.dialog("🎓 Presentación del Proyecto", width="large")
def mostrar_presentacion_proyecto():
    # Leer archivo HTML
    with open('presentacion_defensa.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Renderizar en iframe
    components.html(html_content, height=800, scrolling=True)
```

### Tecnologías Utilizadas

- **Streamlit**: `st.dialog()` para modal
- **Streamlit Components**: `components.html()` para HTML embebido
- **HTML5**: Presentación completa con CSS inline
- **Session State**: Control de estado del modal

---

## 📱 Modos de Visualización

### Opción 1: Modal en Dashboard (Recomendado para demostración rápida)

✅ **Ventajas:**
- Integrado en el sistema
- Acceso inmediato
- No requiere cambiar ventanas

⚠️ **Limitaciones:**
- Altura limitada a 800px (scroll vertical necesario)
- Menor espacio que pantalla completa

**Uso ideal:**
- Demostraciones rápidas
- Revisión de contenido
- Presentación en reuniones virtuales

---

### Opción 2: HTML Externo (Recomendado para defensa formal)

✅ **Ventajas:**
- Pantalla completa real
- Mejor experiencia visual
- Optimizado para proyector

**Cómo acceder:**
```powershell
# Opción A: Desde navegador
start http://localhost:8501

# Opción B: Abrir HTML directamente
start presentacion_defensa.html

# Opción C: Desde VS Code
# Click derecho en presentacion_defensa.html → Open with Live Server
```

**Uso ideal:**
- Defensa del proyecto formal
- Presentación en aula con proyector
- Evento de graduación

---

## 🎬 Flujo de Uso Durante la Defensa

### Escenario 1: Demo del Dashboard + Presentación Integrada

```
1. Abrir dashboard (http://localhost:8501)
2. Demostrar funcionalidades principales:
   - Búsqueda de jugadores
   - Análisis de mercado
   - Predicción ML
3. Hacer clic en "🎓 Ver Presentación"
4. Explicar contexto del proyecto usando el modal
5. Cerrar modal y continuar con demostración
```

**Tiempo estimado**: 30-35 minutos

---

### Escenario 2: Presentación Formal + Demo del Dashboard

```
1. Abrir presentacion_defensa.html en pantalla completa (F11)
2. Recorrer las 11 secciones de la presentación (20-25 min)
3. Abrir dashboard en otra pestaña
4. Demostrar sistema funcionando en vivo (5-10 min)
5. Mencionar que presentación también está embebida en dashboard
```

**Tiempo estimado**: 25-35 minutos

---

## 🐛 Solución de Problemas

### El botón no aparece

**Solución:**
```powershell
# Reconstruir frontend
cd docker
docker-compose build frontend
docker-compose up -d frontend
```

### El modal está vacío o da error

**Verificar que el archivo existe:**
```powershell
# Desde la raíz del proyecto
Test-Path "frontend/presentacion_defensa.html"
# Debe retornar: True
```

**Si retorna False, copiar el archivo:**
```powershell
Copy-Item "presentacion_defensa.html" "frontend/presentacion_defensa.html"
```

### El HTML no se renderiza correctamente

**Causa probable**: Contenido HTML muy grande para componente

**Solución temporal**:
- Usar la presentación HTML externa (`presentacion_defensa.html`)
- O reducir altura del iframe si es necesario

### El modal no se cierra

**Solución:**
- Hacer clic fuera del modal
- Presionar ESC
- Refrescar la página (F5)

---

## 📚 Documentación Relacionada

- **`PRESENTACION_DEFENSA.md`** - Guía completa de la presentación HTML
- **`README.md`** - Documentación técnica del proyecto
- **`presentacion_defensa.html`** - Archivo de presentación original

---

## 🎓 Tips para la Defensa

### Para Máxima Profesionalidad

1. **Antes de la defensa:**
   - Probar ambos modos (modal + HTML externo)
   - Verificar que el dashboard esté corriendo
   - Tener preparadas ambas ventanas

2. **Durante la presentación:**
   - Comenzar con HTML externo en pantalla completa
   - Después demostrar el sistema funcionando
   - Mostrar que la presentación está embebida en el dashboard

3. **Para preguntas:**
   - Usar el modal para referenciar secciones específicas
   - Ejemplo: "Como pueden ver en la sección de ML..." → Abrir modal → Scroll a sección ML

---

## ✅ Checklist de Verificación

Antes de la defensa, verificar:

- [ ] Dashboard corriendo en `http://localhost:8501`
- [ ] Botón "🎓 Ver Presentación" visible en la parte superior
- [ ] Modal se abre correctamente al hacer clic
- [ ] HTML se renderiza completo dentro del modal
- [ ] Scroll funciona dentro del modal
- [ ] Menú de navegación del HTML funciona
- [ ] `presentacion_defensa.html` existe en carpeta `frontend/`
- [ ] Presentación HTML externa también funciona (backup)

---

## 🚀 Comandos Rápidos

```powershell
# Levantar todo el sistema
cd docker
docker-compose up -d

# Verificar que esté corriendo
docker ps | Select-String "fifa"

# Ver logs del frontend
docker logs fifa-frontend --tail 20

# Reconstruir solo frontend (si hay cambios)
docker-compose build frontend
docker-compose up -d frontend

# Abrir dashboard
start http://localhost:8501

# Abrir presentación externa (backup)
start presentacion_defensa.html
```

---

## 🎉 Resultado Final

**Ahora tienes 2 formas de acceder a la presentación:**

1. **🎯 Integrada en Dashboard** (modal) - Para demos y revisiones
2. **🖥️ HTML Externo** (pantalla completa) - Para defensa formal

**¡Sistema completo listo para la defensa del Proyecto de Graduación!** 🎓⚽🚀

---

**Equipo - Grupo 7**  
Universidad Regional Autónoma de los Andes (UniAndes)  
Ingeniería de Software  
Noviembre 2025
