import redis
import IP2Location
import json
from concurrent.futures import ThreadPoolExecutor


database = IP2Location.IP2Location('IP2LOCATION-LITE-DB3.BIN')

database.original_ip = ''


def generate_data():
    try:
        for record in database:
            yield record.__dict__  
    except Exception as e:
        print(f"Error al iterar sobre la base de datos: {e}")


def store_in_redis(item):
    ip = item.get('ip')
    if ip:
        json_data = json.dumps(item)  
        redis_client.set(ip, json_data)  


redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    password="a97f7a7c3c7101d9d15c55e6fba8a2bf393bf05489ace790f8606414668d538c"
)


with ThreadPoolExecutor(max_workers=10) as executor:
    for item in generate_data():
        executor.submit(store_in_redis, item)

print("Datos almacenados en Redis con éxito.")
