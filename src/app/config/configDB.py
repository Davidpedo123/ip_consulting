import redis
import os



redis_client = None

try:
    PORT_REDIS = os.environ.get('PORT_REDIS')
    HOST_REDIS = os.environ.get('HOST_REDIS')
    PASSWD_REDIS = os.environ.get('PASSWD_REDIS', '')
    
    if PORT_REDIS and HOST_REDIS:
        redis_client = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, db=0, password=PASSWD_REDIS)
except Exception as e:
    print(f"Error al conectar a Redis: {e}")