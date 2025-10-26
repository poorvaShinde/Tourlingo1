import requests
from typing import List, Dict
import os

class GoogleMapsHelper:
    def __init__(self, api_key: str = None):
        """Initialize with Google Maps API key"""
        self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.base_url = "https://maps.googleapis.com/maps/api"
    
    def search_places(self, query: str, location: str = None, radius: int = 5000) -> List[Dict]:
        """
        Search for places using Google Places API
        
        Args:
            query: Search query (e.g., "restaurants", "museum")
            location: Center point as "lat,lng"
            radius: Search radius in meters
        
        Returns:
            List of place dictionaries
        """
        endpoint = f"{self.base_url}/place/textsearch/json"
        
        params = {
            'query': query,
            'key': self.api_key
        }
        
        if location:
            params['location'] = location
            params['radius'] = radius
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return self._format_places(data['results'])
            else:
                print(f"Maps API error: {data['status']}")
                return []
                
        except Exception as e:
            print(f"Error searching places: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a specific place"""
        endpoint = f"{self.base_url}/place/details/json"
        
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': 'name,rating,formatted_address,opening_hours,photos,reviews'
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data['result']
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
    
    def geocode_address(self, address: str) -> Dict:
        """Convert address to lat/lng coordinates"""
        endpoint = f"{self.base_url}/geocode/json"
        
        params = {
            'address': address,
            'key': self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': data['results'][0]['formatted_address']
                }
            else:
                return {}
                
        except Exception as e:
            print(f"Error geocoding: {e}")
            return {}
    
    def _format_places(self, places: List) -> List[Dict]:
        """Format place results for easier consumption"""
        formatted = []
        
        for place in places[:10]:  # Limit to top 10
            formatted.append({
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'rating': place.get('rating'),
                'place_id': place.get('place_id'),
                'types': place.get('types', []),
                'location': place.get('geometry', {}).get('location', {})
            })
        
        return formatted
