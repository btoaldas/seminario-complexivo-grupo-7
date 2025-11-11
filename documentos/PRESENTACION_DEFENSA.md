# 🎓 Presentación de Defensa del Proyecto

## ⚽ Sistema de Scouting y Valoración de Jugadores FIFA

Esta es la **presentación oficial onepage** para la defensa del Proyecto de Graduación (Seminario Complexivo) - Grupo 7.

---

## 📋 Descripción

Presentación profesional de pantalla completa diseñada específicamente para la **defensa del proyecto final de graduación** de Ingeniería de Software en UniAndes.

### ✨ Características

- **9 secciones de pantalla completa** adaptadas para proyector
- **Navegación fluida** con scroll smooth y menú fijo
- **Diseño moderno** con gradientes y animaciones
- **Contenido completo** del proyecto (contexto, problema, datos, ML, metodología, resultados)
- **Responsive** - Se adapta a diferentes tamaños de pantalla
- **Sin dependencias externas** - HTML puro autónomo

---

## 🚀 Cómo Usar la Presentación

### Opción 1: Abrir directamente en navegador (Recomendado)

```powershell
# Desde la raíz del proyecto
start presentacion_defensa.html
```

O simplemente **doble clic** en el archivo `presentacion_defensa.html` en el explorador de Windows.

### Opción 2: Servidor local (para mejor performance)

```powershell
# Con Python
python -m http.server 8080

# Luego abrir en navegador:
# http://localhost:8080/presentacion_defensa.html
```

### Opción 3: VS Code Live Server

1. Instalar extensión **Live Server** en VS Code
2. Click derecho en `presentacion_defensa.html`
3. Seleccionar **"Open with Live Server"**

---

## 🎯 Navegación Durante la Defensa

### Menú de Navegación (Esquina superior derecha)

Haz clic en cualquier sección para saltar directamente:

- **Inicio** - Portada con título y autores
- **Contexto** - Información académica del proyecto
- **Problema** - Definición del problema y solución
- **Datos** - Dataset y variables
- **ML** - Comparación de modelos y selección
- **Metodología** - 6 fases del proyecto
- **Resultados** - Logros y métricas
- **Equipo** - Información del equipo y universidad

### Navegación con Teclado

- **Scroll** o **Flechas** ↓↑ - Desplazarse entre secciones
- **Ctrl + Click** en enlaces - Saltar a sección específica
- **F11** - Modo pantalla completa (presentación)

---

## 📊 Estructura de la Presentación

### Sección 1: Portada (Gradiente Morado)
- Título del proyecto
- Universidad UniAndes
- Autores del Grupo 7
- Fecha: Noviembre 2025

### Sección 2: Contexto Académico (Gradiente Rosa)
- Asignatura: Analítica con Python
- Tema del caso
- Tipo de problema: Aprendizaje Supervisado - Regresión
- Objetivo académico
- Equipo de trabajo
- Alcance del proyecto

### Sección 3: Definición del Problema (Gradiente Azul)
- Problemática principal (122,000+ jugadores)
- Solución propuesta (ML para identificar infravalorados)
- Variable objetivo: valor_mercado_eur

### Sección 4: Dataset y Variables (Gradiente Amarillo-Rosa)
- 122,501 jugadores únicos
- 73 columnas procesadas
- 7 versiones FIFA (2015-2021)
- 84 features ML
- Fuente: Kaggle
- Variables principales y features creadas

### Sección 5: Machine Learning (Gradiente Azul Oscuro)
- Comparación de 2 modelos:
  - Regresión Lineal: 35-45% (baseline)
  - **Random Forest: 65-98%** ⭐ GANADOR
- Configuración del modelo ganador
- Justificación de la elección

### Sección 6: Metodología - 6 Fases (Gradiente Verde-Rosa)
1. **Pipeline de Limpieza** (Pandas, NumPy)
2. **EDA** (Jupyter, Plotly)
3. **Entrenamiento ML** (Scikit-learn, Joblib)
4. **API REST** (FastAPI, Uvicorn)
5. **Dashboard** (Streamlit, Plotly)
6. **Docker** (Producción)

Cada fase incluye:
- Tecnologías utilizadas
- Proceso detallado
- Salidas generadas

### Sección 7: Stack Tecnológico (Gradiente Púrpura)
- 8 categorías de tecnologías
- Versiones específicas de cada librería
- Core Python, Data Processing, ML, Backend, Frontend, DevOps

### Sección 8: Resultados (Gradiente Rosa-Amarillo)
- Precisión: 65-98%
- Performance: <1 segundo
- Cobertura: 122,501 jugadores
- Sistema dockerizado
- Métricas del modelo
- Casos de uso

### Sección 9: Arquitectura (Gradiente Morado)
- 4 capas del sistema:
  1. Capa de Datos
  2. Capa de Procesamiento
  3. Capa de Aplicación
  4. Capa de Usuarios
- Ventajas del despliegue Docker

### Sección 10: Conclusiones (Gradiente Azul)
- 8 conclusiones clave del proyecto
- Logros académicos y técnicos
- Competencias demostradas

### Sección 11: Footer (Negro)
- Equipo completo
- Universidad UniAndes
- Carrera: Ingeniería de Software
- Noviembre 2025

---

## 🎨 Diseño Visual

### Paleta de Colores por Sección

| Sección | Gradiente | Propósito |
|---------|-----------|-----------|
| Portada | Morado (667eea → 764ba2) | Elegancia y profesionalismo |
| Contexto | Rosa-Rojo (f093fb → f5576c) | Calidez académica |
| Problema | Azul (4facfe → 00f2fe) | Claridad y confianza |
| Datos | Amarillo-Rosa (fa709a → fee140) | Energía y datos |
| ML | Azul Oscuro (30cfd0 → 330867) | Tecnología y profundidad |
| Metodología | Verde-Rosa (a8edea → fed6e3) | Proceso sistemático |
| Tecnologías | Púrpura (fbc2eb → a6c1ee) | Innovación tecnológica |
| Resultados | Rosa-Amarillo (ff9a9e → fecfef) | Éxito y logros |
| Arquitectura | Morado (667eea → 764ba2) | Estructura sólida |
| Conclusiones | Azul (4facfe → 00f2fe) | Claridad final |

### Elementos de Diseño

- ✅ **Tarjetas con glass-morphism** (backdrop-filter)
- ✅ **Sombras suaves** para profundidad
- ✅ **Animaciones fadeInUp** al cargar
- ✅ **Hover effects** en tarjetas
- ✅ **Tipografía Segoe UI** (profesional)
- ✅ **Iconos emoji** para visual impact
- ✅ **Grid responsive** para adaptabilidad

---

## 📱 Adaptabilidad

### Resoluciones Soportadas

- **Proyector Full HD** (1920x1080) - Óptimo
- **Pantalla 4K** (3840x2160) - Excelente
- **Laptop** (1366x768) - Bueno
- **Tablet** (1024x768) - Adaptable
- **Móvil** (responsive) - Funcional

### Modo Presentación Recomendado

```
1. Abrir en navegador (Chrome/Edge recomendados)
2. Presionar F11 para pantalla completa
3. Conectar proyector
4. Usar scroll o flechas para navegar
5. Menú fijo siempre visible para saltos rápidos
```

---

## 💡 Tips para la Defensa

### Antes de la Presentación

- ✅ Probar en el proyector del aula
- ✅ Verificar que se vean bien los colores
- ✅ Ajustar zoom del navegador si es necesario (Ctrl + / Ctrl -)
- ✅ Cerrar pestañas innecesarias
- ✅ Desactivar notificaciones de Windows

### Durante la Defensa

1. **Portada (30 seg)**: Saludo y presentación del equipo
2. **Contexto (1 min)**: Marco académico del proyecto
3. **Problema (2 min)**: Explicar la problemática y solución ML
4. **Datos (2 min)**: Mostrar estadísticas clave del dataset
5. **Machine Learning (3 min)**: Comparar modelos, justificar Random Forest
6. **Metodología (5 min)**: Explicar las 6 fases con detalle
7. **Tecnologías (1 min)**: Mostrar stack completo
8. **Resultados (3 min)**: Demostrar logros y métricas
9. **Arquitectura (2 min)**: Explicar arquitectura Docker
10. **Conclusiones (2 min)**: Resaltar aprendizajes clave

**Tiempo total estimado**: 20-25 minutos

### Preguntas Comunes a Anticipar

**P: ¿Por qué Random Forest y no otro modelo?**  
R: Sección ML explica 6 ventajas (no lineal, robusto ante outliers, maneja categóricas, etc.)

**P: ¿Cómo manejaron el desbalance de datos?**  
R: Sección Metodología - Fase 1 explica imputación por posición

**P: ¿El sistema está listo para producción?**  
R: Sección Arquitectura muestra despliegue Docker completo

**P: ¿Qué precisión tiene el modelo?**  
R: Sección ML y Resultados: R²=0.65-0.98 (65-98%)

---

## 🔧 Personalización

Si necesitas ajustar contenido, edita `presentacion_defensa.html`:

### Cambiar Colores

Busca las secciones y modifica los gradientes:

```css
#portada {
    background: linear-gradient(135deg, #COLOR1 0%, #COLOR2 100%);
}
```

### Añadir Imágenes

Agrega imágenes en cualquier sección:

```html
<img src="ruta/imagen.png" style="max-width: 800px; border-radius: 20px;">
```

### Modificar Contenido

Cada sección tiene su propio `<section id="nombre">` que puedes editar directamente.

---

## 📦 Archivos Relacionados

- **`presentacion_defensa.html`** - Presentación principal (este archivo)
- **`README.md`** - Documentación técnica del proyecto completo
- **`PRESENTACION_EXPOSICION.md`** - Guía de exposición original

---

## 👥 Equipo - Grupo 7

- **Alberto Alexander Aldás Villacrés**
- **Cristian Joel Riofrío Medina**
- **Wilson Fernando Saavedra Álvarez**

**Universidad Regional Autónoma de los Andes (UniAndes)**  
**Carrera**: Ingeniería de Software  
**Asignatura**: Analítica con Python  
**Proyecto**: Sistema de Scouting y Valoración de Jugadores FIFA  
**Fecha**: Noviembre 2025

---

## 📝 Notas Técnicas

- **Formato**: HTML5 autónomo (sin archivos externos)
- **CSS**: Inline en `<style>` para portabilidad
- **JavaScript**: Mínimo (solo smooth scroll)
- **Compatibilidad**: Chrome 90+, Edge 90+, Firefox 88+
- **Tamaño**: ~70KB (ultra ligero)
- **Carga**: Instantánea (no requiere internet)

---

**⚽ ¡Éxito en la defensa del proyecto! 🚀🎓**
