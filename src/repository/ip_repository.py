import os
import json
import IP2Location
import geoip2.database
import sqlite3
from typing import Optional, List, Dict, Any

class IPRepository:
    """
    Repository for interacting with IP databases (IP2Location, GeoIP2) and Redis cache.
    """
    def __init__(self, redis_client=None):
        """
        Initializes the repository with paths to BIN and MMDB databases.
        """
        self.redis_client = redis_client
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db4_path = os.path.join(base_path, 'data', 'IP2LOCATION-LITE-DB3.BIN')
        self.db6_path = os.path.join(base_path, 'data', 'DB1_IP6.BIN')
        self.geoip_db_path = os.path.join(base_path, 'data', 'GeoLite2-City.mmdb')
        self.sqlite_db_path = os.path.join(base_path, 'data', 'unified_data.db')

    def get_from_cache(self, ip: str):
        """
        Retrieves IP data from Redis cache.
        """
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(ip)
                if cached_data:
                    return json.loads(cached_data.decode("UTF-8"))
            except Exception as e:
                print(f"Error al consultar Redis: {e}")
        return None

    def get_many_from_cache(self, ips: list[str]):
        """
        Retrieves multiple IP records from Redis cache in bulk.
        """
        if self.redis_client:
            try:
                cached_values = self.redis_client.mget(ips)
                results = {}
                for ip, val in zip(ips, cached_values):
                    if val:
                        results[ip] = json.loads(val.decode("UTF-8"))
                return results
            except Exception as e:
                print(f"Error en mget de Redis: {e}")
        return {}

    def save_to_cache(self, ip: str, data: dict):
        """
        Saves a single IP record to Redis cache.
        """
        if self.redis_client:
            try:
                self.redis_client.set(ip, json.dumps(data))
            except Exception as e:
                print(f"Error al guardar en Redis: {e}")

    def save_many_to_cache(self, mapping: dict[str, dict]):
        """
        Saves multiple IP records to Redis cache using a pipeline.
        """
        if self.redis_client and mapping:
            try:
                pipeline = self.redis_client.pipeline()
                for ip, data in mapping.items():
                    pipeline.set(ip, json.dumps(data))
                pipeline.execute()
            except Exception as e:
                print(f"Error en mset/pipeline de Redis: {e}")

    def get_from_bin(self, ip: str):
        """
        Retrieves IP data from BIN (IP2Location) and MMDB (GeoIP2) files and merges them.
        """
        try:
            if len(ip) > 15:
                database = IP2Location.IP2Location(self.db6_path)
                print(f"Consultando Base de datos IP6: {self.db6_path}")
            else:
                database = IP2Location.IP2Location(self.db4_path)
                print(f"Consultando Base de datos IP4: {self.db4_path}")
            
            result = database.get_all(ip).__dict__
            
            # Consultar coordenadas en GeoIP2 (MMDB)
            try:
                if os.path.exists(self.geoip_db_path):
                    with geoip2.database.Reader(self.geoip_db_path) as reader:
                        response = reader.city(ip)
                        result['latitude'] = response.location.latitude
                        result['longitude'] = response.location.longitude
                else:
                    print(f"Base de datos GeoIP2 no encontrada en: {self.geoip_db_path}")
                    result['latitude'] = 0.0
                    result['longitude'] = 0.0
            except Exception as e:
                print(f"Error al consultar GeoIP2 (MMDB): {e}")
                result['latitude'] = 0.0
                result['longitude'] = 0.0

            return result
        except Exception as e:
            print(f"Error al consultar base de datos BIN: {e}")
            raise e

    def search(self, query: Optional[str] = None, country: Optional[str] = None, 
               region: Optional[str] = None, city: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Searches for locations in the unified SQLite index by keywords.
        """
        if not os.path.exists(self.sqlite_db_path):
            print(f"Búsqueda abortada: El índice SQLite no existe en {self.sqlite_db_path}")
            return []

        conn = None
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            sql = "SELECT country_name, region_name, city_name, latitude, longitude FROM ip_index WHERE 1=1"
            params: List[Any] = []

            if query:
                sql += " AND (city_name LIKE ? OR region_name LIKE ? OR country_name LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
            
            if country:
                sql += " AND country_name LIKE ?"
                params.append(f"%{country}%")
            
            if region:
                sql += " AND region_name LIKE ?"
                params.append(f"%{region}%")
            
            if city:
                sql += " AND city_name LIKE ?"
                params.append(f"%{city}%")

            sql += " LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error en búsqueda SQLite: {e}")
            return []
        finally:
            if conn:
                conn.close()
        return []
