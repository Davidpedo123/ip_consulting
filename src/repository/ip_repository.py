import os
import json
import IP2Location

class IPRepository:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db4_path = os.path.join(base_path, 'data', 'IP2LOCATION-LITE-DB3.BIN')
        self.db6_path = os.path.join(base_path, 'data', 'DB1_IP6.BIN')

    def get_from_cache(self, ip: str):
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(ip)
                if cached_data:
                    return json.loads(cached_data.decode("UTF-8"))
            except Exception as e:
                print(f"Error al consultar Redis: {e}")
        return None

    def get_many_from_cache(self, ips: list[str]):
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
        if self.redis_client:
            try:
                self.redis_client.set(ip, json.dumps(data))
            except Exception as e:
                print(f"Error al guardar en Redis: {e}")

    def save_many_to_cache(self, mapping: dict[str, dict]):
        if self.redis_client and mapping:
            try:
                pipeline = self.redis_client.pipeline()
                for ip, data in mapping.items():
                    pipeline.set(ip, json.dumps(data))
                pipeline.execute()
            except Exception as e:
                print(f"Error en mset/pipeline de Redis: {e}")

    def get_from_bin(self, ip: str):
        try:
            if len(ip) > 15:
                database = IP2Location.IP2Location(self.db6_path)
                print(f"Consultando Base de datos IP6: {self.db6_path}")
            else:
                database = IP2Location.IP2Location(self.db4_path)
                print(f"Consultando Base de datos IP4: {self.db4_path}")
            
            return database.get_all(ip).__dict__
        except Exception as e:
            print(f"Error al consultar base de datos BIN: {e}")
            raise e
