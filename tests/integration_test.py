import requests

BASE_URL = "http://localhost:8888"

def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "API para Scoring activa"}

def test_scoring():
    data = {"data": [[1.5, 2.3, "Tuesday", 4.2, 5.1, "Oregon", "toyota"]]}
    response = requests.post(f"{BASE_URL}/score", json=data)
    assert response.status_code == 200
    assert "predictions" in response.json()
