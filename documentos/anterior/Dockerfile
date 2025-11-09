# Imagen para servir la API de Scouting FIFA
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Guayaquil

# Instalar tzdata para zona horaria
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias
COPY src/api/requirements.txt /app/src/api/requirements.txt
COPY requirements_dashboard.txt /app/requirements_dashboard.txt
RUN pip install --no-cache-dir -r /app/src/api/requirements.txt \
    && pip install --no-cache-dir -r /app/requirements_dashboard.txt

# Copiar código y modelos necesarios para inferencia
COPY src /app/src
COPY models /app/models
COPY dashboard_streamlit.py /app/dashboard_streamlit.py

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
