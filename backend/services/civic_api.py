import requests
from config import Config

# get representatives by the user's area
def fetch_reps(zip_code):
    url = f"https://www.googleapis.com/civicinfo/v2/representatives?address={zip_code}&key={Config.CIVIC_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "fetch failed for getting representatives"}
    return response.json()