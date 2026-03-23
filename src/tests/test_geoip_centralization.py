import pytest
from src.repository.ip_repository import IPRepository
import os

def test_centralize_ip_data():
    """
    Test que verifica la centralización de datos: IP2Location (Ciudad) + GeoIP2 (Coordenadas)
    """
    repo = IPRepository()
    ip_test = "8.8.8.8"
    
    # Realizar la consulta
    data = repo.get_from_bin(ip_test)
    
    print(f"\nDatos centralizados para {ip_test}:")
    print(data)
    
    # Verificaciones
    assert "ip" in data
    assert "city" in data
    assert "latitude" in data
    assert "longitude" in data
    
    # Para 8.8.8.8 usualmente la ciudad es Mountain View o similar, y tiene coordenadas
    assert data["latitude"] != 0.0
    assert data["longitude"] != 0.0
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)

if __name__ == "__main__":
    test_centralize_ip_data()
