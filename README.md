# RepTracker
Track your representatives. Hold them accountable to your vote.
This project allows users to find their local congressional representatives, analyze voting records/statements, & generate AI-based summaries using Google Gemini.

## Features

- Fetch representatives by ZIP code via Google Civic API
- Retrieve voting & statement data per representative
- Summarize long political content using Gemini API
- Utilizes SQLite (via SQLAlchemy) for easy local storage and future expansion
### NOTE ^ decide what DB to use here sqlite or supabase

## 🛠️ Setup Instructions
1. clone the repo
```bash
git clone https://github.com/your-username/track-your-reps.git
cd track-your-reps/backend
```
2. Create local environment
```
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Run the app
```
python app.py
```
### Frontend Side
- idk since we haven't decided html or react

