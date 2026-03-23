import pytest
from src import namespace
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_get_ip_success():
    response = client.get("/get-ip?ip=8.8.8.8")
    assert response.status_code == 200
    json_data = response.json()
    assert "ip" in json_data
    assert json_data["ip"]["country_short"] == "US"

def test_get_ip_invalid_format():
    response = client.get("/get-ip?ip=not-an-ip")
    assert response.status_code == 400
    assert "Invalid IP address format" in response.json()["detail"]

def test_get_ip_not_found():
    response = client.get("/get-ip?ip=192.168.1.1")
    assert response.status_code in [200, 404, 400]

def test_get_ip_missing_param():
    response = client.get("/get-ip")
    assert response.status_code == 422
