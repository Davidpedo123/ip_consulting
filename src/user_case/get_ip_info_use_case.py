import time
import ipaddress
from fastapi import HTTPException

class GetIPInfoUseCase:
    def __init__(self, ip_repository):
        self.ip_repository = ip_repository

    def execute(self, ip: str):
        self.validate_ip(ip)

        data = None
        
        redis_start_time = time.time()
        data = self.ip_repository.get_from_cache(ip)
        if data:
            redis_duration = time.time() - redis_start_time
            print(f"Tiempo de respuesta de Redis: {redis_duration:.6f} segundos")
            return data

        db_start_time = time.time()
        data = self.ip_repository.get_from_bin(ip)
        db_duration = time.time() - db_start_time
        print(f"Tiempo de respuesta de la base de datos BIN: {db_duration:.6f} segundos")

        if data:
            self.ip_repository.save_to_cache(ip, data)
        
        return data

    @staticmethod
    def validate_ip(ip: str):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid IP address format: {ip}")

    @staticmethod
    def check_invalid_ip(data):
        if not data:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        for key, value in data.items():
            if isinstance(value, str):
                if "INVALID IP ADDRESS" in value:
                    raise HTTPException(status_code=400, detail="Invalid IP address value in the record")
                elif "-" == value:
                    pass
        return data
