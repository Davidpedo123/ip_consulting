import time
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
from src.user_case.get_ip_info_use_case import GetIPInfoUseCase

class GetBulkIPInfoUseCase:
    def __init__(self, ip_repository):
        self.ip_repository = ip_repository

    def execute(self, ips: list[str]):
        unique_ips = list(set(ips))
        for ip in unique_ips:
            GetIPInfoUseCase.validate_ip(ip)

        results = self.ip_repository.get_many_from_cache(unique_ips)
        
        missing_ips = [ip for ip in unique_ips if ip not in results]
        
        if missing_ips:
            with ThreadPoolExecutor(max_workers=10) as executor:
                bin_results = list(executor.map(self.ip_repository.get_from_bin, missing_ips))
            
            new_results_map = {}
            for ip, data in zip(missing_ips, bin_results):
                if data:
                    results[ip] = data
                    new_results_map[ip] = data
            
            if new_results_map:
                self.ip_repository.save_many_to_cache(new_results_map)

        return {ip: results.get(ip) for ip in ips}
