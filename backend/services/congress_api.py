import requests
from config import Config
def fetch_rep_activity(rep_id):
    # return what rep been doin
    url = f"https://api.congress.gov/v3/member/{rep_id}/sponsored-legislation?api_key={Config.CONGRESS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "fetch failed for getting data on representatives"}
    return response.json()

def get_bill_summary(congress, billType, billNumber):
    url = f"https://api.congress.gov/v3/bill/{congress}/{billType}/{billNumber}/summaries?api_key={Config.CONGRESS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "fetch failed for getting data on representatives"}
    return response.json()