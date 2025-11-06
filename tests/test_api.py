"""
Pruebas básicas de la API FastAPI.

- Verifica que /health responda 200 y tenga campos esperados.
- Valida /predict cuando los artefactos del modelo están disponibles.
"""

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def modelos_disponibles() -> bool:
    base = Path(__file__).resolve().parents[1]
    return (base / "models" / "modelo_valoracion_fifa.pkl").exists() and (
        base / "models" / "columnas_modelo.pkl"
    ).exists()


def dataset_disponible() -> bool:
    base = Path(__file__).resolve().parents[1]
    return (base / "data" / "processed" / "fifa_limpio.csv").exists()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data and "timestamp" in data


def test_request_id_header_present():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert "x-request-id" in {k.lower(): v for k, v in resp.headers.items()}


@pytest.mark.skipif(
    not modelos_disponibles(), reason="Modelos no encontrados en carpeta models/"
    )
def test_predict_ok():
    payload = {
        "edad": 24,
        "calificacion_general": 78,
        "potencial": 84,
        "altura_cm": 180,
        "peso_kg": 75,
        "posicion_principal": "ST",
        "pie_preferido": "Right",
        "id_jugador": "test-1",
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id_jugador"] == "test-1"
    assert isinstance(data["valor_estimado"], (int, float))


@pytest.mark.skipif(
    not modelos_disponibles(), reason="Modelos no encontrados en carpeta models/"
)
def test_predict_batch_ok():
    payload = [
        {
            "edad": 24,
            "calificacion_general": 78,
            "potencial": 84,
            "altura_cm": 180,
            "peso_kg": 75,
            "posicion_principal": "ST",
            "pie_preferido": "Right",
            "id_jugador": "test-1",
        },
        {
            "edad": 20,
            "calificacion_general": 72,
            "potencial": 85,
            "altura_cm": 175,
            "peso_kg": 70,
            "posicion_principal": "CM",
            "pie_preferido": "Left",
            "id_jugador": "test-2",
        },
    ]
    resp = client.post("/predict_batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 2
    assert data[0]["id_jugador"] == "test-1"
    assert data[1]["id_jugador"] == "test-2"


@pytest.mark.skipif(
    not (modelos_disponibles() and dataset_disponible()),
    reason="Modelos o dataset procesado no encontrados",
)
def test_oportunidades_infravaloradas():
    resp = client.get("/oportunidades_infravaloradas?top_n=5&min_valor_real=500000")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        item = data[0]
        # Debe incluir campos formateados en euros
        assert "valor_real_formateado" in item
        assert "valor_predicho_formateado" in item
        assert "oportunidad_eur_formateado" in item


@pytest.mark.skipif(
    not (modelos_disponibles() and dataset_disponible()),
    reason="Modelos o dataset procesado no encontrados",
)
def test_top_sobrevalorados():
    resp = client.get("/top_sobrevalorados?top_n=5&min_valor_real=500000")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 5
