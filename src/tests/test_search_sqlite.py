import pytest
from src.repository.ip_repository import IPRepository

def test_search_by_city_proximity():
    """
    Validates that searching by a partial city name (e.g. 'Mount') returns results.
    """
    repo = IPRepository()
    
    # Searching for 'Mount' (proximity search for Mountain View, etc.)
    results = repo.search(query="Mount", limit=5)
    
    print("\nResultados para búsqueda 'Mount':")
    for res in results:
        print(res)
        
    assert len(results) > 0
    assert any("Mount" in res['city_name'] for res in results)
    assert "latitude" in results[0]
    assert "longitude" in results[0]

def test_search_by_region():
    """
    Validates filtering by region (e.g. 'California').
    """
    repo = IPRepository()
    
    results = repo.search(region="California", limit=10)
    
    assert len(results) > 0
    for res in results:
        assert res['region_name'] == "California"

def test_search_limit():
    """
    Validates that the limit argument is respected.
    """
    repo = IPRepository()
    
    limit = 3
    results = repo.search(query="United States", limit=limit)
    
    assert len(results) <= limit

def test_search_not_found():
    """
    Validates behavior when no results are found.
    """
    repo = IPRepository()
    
    results = repo.search(query="NonExistentCityXYZ", limit=5)
    
    assert len(results) == 0

if __name__ == "__main__":
    test_search_by_city_proximity()
    test_search_by_region()
    test_search_limit()
    test_search_not_found()
    print("All search tests passed!")
