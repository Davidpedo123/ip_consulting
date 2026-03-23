import pytest
from src import namespace
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_get_ips_bulk_success():
    ips = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
    response = client.post("/get-ips", json={"ips": ips})
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 3
    assert json_data["8.8.8.8"]["country_short"] == "US"
    assert json_data["1.1.1.1"]["country_short"] == "AU"

def test_get_ips_bulk_duplicates():
    # En un diccionario, las claves duplicadas se colapsan, lo cual es eficiente
    ips = ["8.8.8.8", "8.8.8.8"]
    response = client.post("/get-ips", json={"ips": ips})
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data["8.8.8.8"]["country_short"] == "US"

def test_get_ips_bulk_invalid_ip():
    ips = ["8.8.8.8", "invalid-ip"]
    response = client.post("/get-ips", json={"ips": ips})
    assert response.status_code == 400
    assert "Invalid IP address format" in response.json()["detail"]

def test_get_ips_bulk_empty_list():
    ips = []
    response = client.post("/get-ips", json={"ips": ips})
    assert response.status_code == 200
    assert response.json() == {}
