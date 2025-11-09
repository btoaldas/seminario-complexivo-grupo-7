# Atajos para desarrollar y ejecutar API y Dashboard
# Requiere tener Python/venv y Docker (opcional) instalados

.PHONY: help install install_api install_dash api dash docker-build up down test fmt lint

PORT ?= 8000
DASH_PORT ?= 8501

help:
	@echo "Targets disponibles:"
	@echo "  install        - Instala API + dashboard"
	@echo "  install_api    - Instala dependencias de la API"
	@echo "  install_dash   - Instala dependencias del dashboard"
	@echo "  api            - Ejecuta la API en http://localhost:$(PORT)"
	@echo "  dash           - Ejecuta el dashboard en http://localhost:$(DASH_PORT)"
	@echo "  docker-build   - Construye imágenes con docker-compose"
	@echo "  up             - Levanta API y dashboard con docker-compose"
	@echo "  down           - Detiene servicios docker-compose"
	@echo "  test           - Ejecuta pruebas (pytest)"
	@echo "  fmt            - Formatea código (isort + black)"
	@echo "  lint           - Lint con ruff"

install: install_api install_dash

install_api:
	pip install -r src/api/requirements.txt

install_dash:
	pip install -r requirements_dashboard.txt

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port $(PORT)

dash:
	streamlit run dashboard_streamlit.py --server.address 0.0.0.0 --server.port $(DASH_PORT)

docker-build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

test:
	pytest -q || true

fmt:
	isort .
	black .

lint:
	ruff check .
