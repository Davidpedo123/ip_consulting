from typing import Optional, List, Dict, Any

class SearchUseCase:
    def __init__(self, ip_repository):
        self.ip_repository = ip_repository

    def execute(self, query: Optional[str] = None, country: Optional[str] = None, 
                region: Optional[str] = None, city: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Executes the search for locations based on keywords.
        """
        # Validate limit
        if not (1 <= limit <= 100):
            limit = 10
            
        return self.ip_repository.search(query=query, country=country, region=region, city=city, limit=limit)
