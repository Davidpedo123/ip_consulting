import sqlite3
import os
import IP2Location
import maxminddb
from tqdm import tqdm

# Global paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DATA_PATH = os.path.join(BASE_PATH, 'repository', 'data')
DB4_PATH = os.path.join(REPO_DATA_PATH, 'IP2LOCATION-LITE-DB3.BIN')
GEOIP_DB_PATH = os.path.join(REPO_DATA_PATH, 'GeoLite2-City.mmdb')
SQLITE_DB_PATH = os.path.join(REPO_DATA_PATH, 'unified_data.db')

def generate_index():
    """
    Versión estable y eficiente en memoria para centralizar los datos en SQLite.
    Procesa el archivo MMDB registro por registro sin cargar todo en RAM.
    """
    print(f"Iniciando indexación segura...")
    print(f"Origen: {DB4_PATH} y {GEOIP_DB_PATH}")
    print(f"Destino: {SQLITE_DB_PATH}")

    # Inicializar base de datos IP2Location
    ip2loc = IP2Location.IP2Location(DB4_PATH)
    
    # Configurar SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ip_index")
    cursor.execute("""
        CREATE TABLE ip_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT,
            region_name TEXT,
            city_name TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    # Optimizaciones básicas para inserción masiva
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = OFF")
    cursor.execute("PRAGMA cache_size = 10000") # 10MB cache
    
    seen_cities = set()
    batch = []
    batch_size = 2000
    total_found = 0
    total_indexed = 0

    try:
        print("Recorriendo registros... Esto puede tardar pero es seguro para los recursos.")
        with maxminddb.open_database(GEOIP_DB_PATH) as reader:
            # El iterador de maxminddb es eficiente y no carga todo el archivo
            for network, data in tqdm(reader, desc="Procesando"):
                total_found += 1
                
                # Filtrar solo registros con información relevante
                if 'city' in data or 'location' in data:
                    sample_ip = str(network.network_address)
                    
                    # Consultar IP2Location
                    loc_data = ip2loc.get_all(sample_ip)
                    
                    country = str(loc_data.country_long)
                    region = str(loc_data.region)
                    city = str(loc_data.city)
                    
                    # Evitar duplicados exactos de Ciudad/Región/País
                    city_key = (country, region, city)
                    if city_key not in seen_cities:
                        lat = data.get('location', {}).get('latitude', 0.0)
                        lon = data.get('location', {}).get('longitude', 0.0)
                        
                        batch.append((country, region, city, lat, lon))
                        seen_cities.add(city_key)
                        total_indexed += 1
                        
                        if len(batch) >= batch_size:
                            cursor.executemany(
                                "INSERT INTO ip_index (country_name, region_name, city_name, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                                batch
                            )
                            batch = []
                            # Limpiar set periódicamente si crece demasiado (opcional, 250k entries son ~50MB)

        # Insertar remanentes
        if batch:
            cursor.executemany(
                "INSERT INTO ip_index (country_name, region_name, city_name, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                batch
            )
        
        print(f"Finalizado. Se encontraron {total_found} rangos y se indexaron {total_indexed} ubicaciones únicas.")
        
        print("Creando índices finales para búsquedas rápidas...")
        cursor.execute("CREATE INDEX idx_city ON ip_index(city_name)")
        cursor.execute("CREATE INDEX idx_region ON ip_index(region_name)")
        cursor.execute("CREATE INDEX idx_country ON ip_index(country_name)")
        
        conn.commit()
        print("Proceso completado exitosamente.")

    except Exception as e:
        print(f"Error durante la indexación: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_index()
