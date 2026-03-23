import os
import pytest
from src import namespace
from src.app.config.configDB import redis_client
from src.repository.ip_repository import IPRepository

def test_redis_connection():
    if redis_client:
        try:
            assert redis_client.ping() is True
        except Exception as e:
            # If it's configured but cannot connect, it's a failure in "test de conexion"
            pytest.fail(f"Redis is configured but cannot connect: {e}")
    else:
        # If not configured, we just skip or it depends on requirements.
        # Given the request, it's good to know if it's missing.
        print("Redis is not configured. Skipping connection test.")

def test_bin_files_exist():
    repo = IPRepository()
    assert os.path.exists(repo.db4_path), f"IPv4 database not found at {repo.db4_path}"
    assert os.path.exists(repo.db6_path), f"IPv6 database not found at {repo.db6_path}"

def test_bin_query_works():
    repo = IPRepository()
    # 8.8.8.8 should be queryable if BIN exists
    result = repo.get_from_bin("8.8.8.8")
    assert result is not None
    assert isinstance(result, dict)
    assert result.get('country_short') == "US"
