import requests
import config from Config
# summarize text
# Note: this is taken from our previous project code so we need to personalize it for this project 
def summarize_text(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={Config.GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Summarize the following text in 2-3 sentences:\n\n{article_text}"
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"