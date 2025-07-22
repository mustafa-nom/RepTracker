import requests
from config import Config

def fetch_rep_activity(rep_id):
    """Fetch sponsored legislation for a representative"""
    if not rep_id:
        return {"error": "No representative ID provided"}
    
    
    # Use the congress API given the rep_id and the api key to fetch data
    try:
        url = f"https://api.congress.gov/v3/member/{rep_id}/sponsored-legislation?api_key={Config.CONGRESS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        # Status code error handling
        if response.status_code == 404:
            return {"error": f"Representative {rep_id} not found"}
        elif response.status_code != 200:
            return {"error": f"Congress API error: {response.status_code}"}
        
        data = response.json()
        if not isinstance(data, dict):
            return {"error": "Invalid response format from Congress API"}
        
        #return the data
        return data
    
    # More error handling
    except requests.exceptions.Timeout:
        return {"error": "Congress API request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_bill_summary(congress, billType, billNumber):
    """Get summary for a specific bill"""
    if not all([congress, billType, billNumber]):
        return {"error": "Missing required parameters"}
    
    # Use the Congress API to get bill data based on the congress, billtype, and billnumber
    try:
        url = f"https://api.congress.gov/v3/bill/{congress}/{billType}/{billNumber}/summaries?api_key={Config.CONGRESS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        # Status code error handling
        if response.status_code == 404:
            return {"summaries": []}
        elif response.status_code != 200:
            return {"error": f"Congress API error: {response.status_code}"}
        
        data = response.json()
        if not isinstance(data, dict):
            return {"error": "Invalid response format from Congress API"}
        
        # Return data
        return data
    
    # More error handling
    except requests.exceptions.Timeout:
        return {"error": "Congress API request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_bill_details(congress, billType, billNumber):
    """Get detailed information for a specific bill including introduction date and latest action"""
    if not all([congress, billType, billNumber]):
        return {"error": "Missing required parameters"}
    
    try:
        # get full bill details
        url = f"https://api.congress.gov/v3/bill/{congress}/{billType}/{billNumber}?api_key={Config.CONGRESS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return {"error": "Bill not found"}
        elif response.status_code != 200:
            return {"error": f"Congress API error: {response.status_code}"}
        
        data = response.json()
        
        bill_data = data.get("bill", {})
        introduced_date = bill_data.get("introducedDate")
        
        latest_action = None
        actions = bill_data.get("actions", {})
        if actions and isinstance(actions, dict):
            # actions usually sorted by date, most recent first
            action_items = actions.get("item", [])
            if action_items and isinstance(action_items, list) and len(action_items) > 0:
                # get first (most recent) action
                latest = action_items[0]
                latest_action = {
                    "text": latest.get("text", ""),
                    "actionDate": latest.get("actionDate", ""),
                    "actionTime": latest.get("actionTime"),
                    "type": latest.get("type", "")
                }
        
        return {
            "introducedDate": introduced_date,
            "latestAction": latest_action,
            "originChamber": bill_data.get("originChamber"),
            "policyArea": bill_data.get("policyArea", {}).get("name") if bill_data.get("policyArea") else None,
            "sponsors": bill_data.get("sponsors"),
            "cosponsors": bill_data.get("cosponsors")
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Congress API request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}