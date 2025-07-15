import requests
from config import Config
from geocodio import GeocodioClient

# get representatives by the user's area
def fetch_reps(zip_code):
    try: 
        print(f"api key: {Config.GEOCODIO_API_KEY}")
        client = GeocodioClient(Config.GEOCODIO_API_KEY)
        location = client.geocode(zip_code, fields=["cd"])
        if not location or not location.coords:
            return {"error": "couldnt get the zip code for geocodio api"}
        return location
    except Exception as e:
        return {"error": f"Geocodio api error: {e}"}