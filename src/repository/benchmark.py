import requests
import time

def benchmark_request(url, ip):
    # Crear la URL con el parámetro IP
    full_url = f"{url}?ip={ip}"
    
    # Registrar el tiempo de inicio
    start_time = time.time()
    
    # Realizar la solicitud a la API
    response = requests.get(full_url)
    
    # Registrar el tiempo de finalización
    end_time = time.time()
    
    # Calcular el tiempo total de la solicitud
    total_time = end_time - start_time
    
    # Verificar si la respuesta es exitosa
    if response.status_code == 200:
        print(f"Tiempo total de respuesta: {total_time:.6f} segundos")
        return response.json()  # Mostrar el resultado de la API
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    # URL de tu API y dirección IP para la prueba
    api_url = "http://localhost/get-ip"
    test_ip = "8.8.2.8"
    
    # Realizar múltiples pruebas
    for i in range(5):
        print(f"Prueba {i+1}:")
        result = benchmark_request(api_url, test_ip)
        print(result)
        print("-" * 40)
