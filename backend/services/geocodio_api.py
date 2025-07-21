import requests
from config import Config
from geocodio import GeocodioClient

def fetch_reps(zip_code):
    """Get representatives by the user's area"""
    if not zip_code:
        return {"error": "No zip code provided"}
    if not zip_code.isdigit() or len(zip_code) != 5:
        return {"error": "Invalid zip code format. Please provide a 5-digit zip code"}
    
    try: 
        print(f"Fetching representatives for zip code: {zip_code}")
        if not Config.GEOCODIO_API_KEY:
            return {"error": "Geocodio API key not configured"}
            
        client = GeocodioClient(Config.GEOCODIO_API_KEY)
        location = client.geocode(zip_code, fields=["cd"])
        if not location:
            return {"error": "No location data returned from Geocodio"}
            
        location_dict = location
        if not location_dict.get("results"):
            return {"error": "No results found for this zip code"}
            
        # congressional district data error handling
        has_cd_data = False
        for result in location_dict.get("results", []):
            if result.get("fields", {}).get("congressional_districts"):
                has_cd_data = True
                break
        if not has_cd_data:
            return {"error": "No congressional district data available for this zip code"}
            
        return location_dict
        
    except ValueError as e:
        return {"error": f"Invalid API key or configuration: {str(e)}"}
    except Exception as e:
        return {"error": f"Geocodio API error: {str(e)}"}