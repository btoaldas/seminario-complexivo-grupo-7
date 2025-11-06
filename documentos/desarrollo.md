# Guía de Desarrollo

## Estándares

- Nomenclatura: `snake_case` sin `ñ` ni tildes en identificadores.
- Comentarios y docstrings en español con tildes.
- Zona horaria: `America/Guayaquil`. Codificación: UTF-8.

## Instalación de herramientas de desarrollo

Opcional, para formateo y lint:

```bash
pip install -r requirements_dev.txt
```

## Tareas comunes (Makefile)

```bash
make install          # API + dashboard
make api              # Ejecuta API (uvicorn)
make dash             # Ejecuta dashboard (streamlit)
make fmt              # isort + black
make lint             # ruff check
make up               # docker compose up (API + dashboard)
```

## Estructura relacionada

```
src/
  api/
    inference.py      # preparación de features e inferencia
    schemas.py        # validación de entrada
  valoracion.py       # utilidades para clasificar (infravalorado/sobrevalorado)
dashboard_streamlit.py # UI Streamlit
documentos/            # documentación
```

