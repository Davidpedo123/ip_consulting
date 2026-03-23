import sys
import os
from typing import Optional

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src import namespace

from fastapi import FastAPI, Request, HTTPException, Query, status
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import ipaddress

from src.app.config.configDB import redis_client
from src.repository.ip_repository import IPRepository
from src.user_case.get_ip_info_use_case import GetIPInfoUseCase
from src.user_case.get_bulk_ip_info_use_case import GetBulkIPInfoUseCase
from src.user_case.search_use_case import SearchUseCase

app = FastAPI(title="IP Consulting API")

class BulkIPRequest(BaseModel):
    ips: list[str]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

ip_repo = IPRepository(redis_client=redis_client)
get_ip_use_case = GetIPInfoUseCase(ip_repository=ip_repo)
get_bulk_ip_use_case = GetBulkIPInfoUseCase(ip_repository=ip_repo)
search_use_case = SearchUseCase(ip_repository=ip_repo)

@app.get("/get-ip")
async def get_ip(ip: str = Query(..., description="The IP address to lookup")):
    try:
        data = get_ip_use_case.execute(ip)
        get_ip_use_case.check_invalid_ip(data)
        return {"ip": data}
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error general en el controlador: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/get-ips")
async def get_ips(request: BulkIPRequest):
    try:
        results = get_bulk_ip_use_case.execute(request.ips)
        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error en bulk lookup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search")
async def search_locations(
    q: Optional[str] = Query(None, description="General keyword search (city, region, or country)"),
    country: Optional[str] = Query(None, description="Filter by country name"),
    region: Optional[str] = Query(None, description="Filter by region name"),
    city: Optional[str] = Query(None, description="Filter by city name"),
    limit: int = Query(10, description="Max number of results", ge=1, le=100)
):
    """
    Search for locations by keywords.
    """
    try:
        results = search_use_case.execute(query=q, country=country, region=region, city=city, limit=limit)
        return {"results": results}
    except Exception as e:
        print(f"Error en endpoint /search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

