import sys
import os

# Añadir la ruta del directorio raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.api import app  # Importa la API de FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API para Scoring activa"}

def test_scoring():
    payload = {"data": [[1.5, 2.3, "Tuesday", 4.2, 5.1, "Oregon", "toyota"]]}
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    assert "predictions" in response.json()

