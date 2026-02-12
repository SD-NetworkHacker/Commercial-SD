import requests
import json
from ..config import Config

class GooglePlacesSearch:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.GOOGLE_PLACES_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    def search(self, location="48.8566,2.3522", radius=5000, keyword="bakery", type=None):
        """
        Search for businesses using Google Places API.
        
        Args:
            location (str): "lat,long" (default: Paris)
            radius (int): Search radius in meters
            keyword (str): Keyword to search for (e.g., "bakery", "plumber")
            type (str): Type of place (optional)
            
        Returns:
            list: List of dicts with keys: name, address, place_id, types, location, rating
        """
        if Config.ANTIGRAVITY_FLIGHT:
            print("🚀 [FLIGHT MODE] Returning mock search results")
            return self._mock_results(keyword)

        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API_KEY is missing")

        params = {
            "location": location,
            "radius": radius,
            "keyword": keyword,
            "key": self.api_key
        }
        
        if type:
            params["type"] = type

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for place in data.get("results", [])[:Config.MAX_PROSPECTS]:
            results.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "place_id": place.get("place_id"),
                "types": place.get("types"),
                "location": place.get("geometry", {}).get("location"),
                "rating": place.get("rating")
            })
            
        return results

    def _mock_results(self, keyword):
        """Return 3 mock results for testing."""
        return [
            {
                "name": f"Le Panier {keyword.capitalize()}",
                "address": "12 Rue de la Paix, 75002 Paris",
                "place_id": "mock_id_1",
                "types": [keyword, "bakery"],
                "website": None, # Will be checked later
                "rating": 4.5
            },
            {
                "name": f"Vieille Boutique {keyword.capitalize()}",
                "address": "45 Avenue des Champs-Elysées, 75008 Paris",
                "place_id": "mock_id_2",
                "types": [keyword, "store"],
                "website": "http://vieille-boutique-1998.com",
                "rating": 3.2
            },
            {
                "name": f"Modern {keyword.capitalize()} Startup",
                "address": "Station F, 75013 Paris",
                "place_id": "mock_id_3",
                "types": [keyword, "tech"],
                "website": "https://modern-startup.io",
                "rating": 4.9
            }
        ]
