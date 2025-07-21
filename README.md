# RepTracker
Track your representatives. Hold them accountable to your vote.  
This project allows users to find their local congressional representatives, analyze voting records/statements, & generate AI-based summaries using Google Gemini.

## Features

- Fetch local representatives by zipcode, identifying congressional districts & legislators via the Geocodio API  
- Retrieve sponsored legislation & bill details for each representative or senator using the Congress.gov API  
- Summarize political content using the Gemini API for quick, AI-generated overviews of bills or statements  
- Store representative and bill data locally with SQLite and SQLAlchemy to enable caching and reduce API calls  
- React frontend integrated with the Flask API for real-time display of legislative activity and summaries


## 🛠️ Setup Instructions
1. clone the repo
```bash
git clone https://github.com/your-username/track-your-reps.git
cd reptracker/backend
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
1. Navigate to frontend directory
```
cd ../frontend
```
2. Install frontend dependencies
```
npm install
```
3. Start the server
```
npm run dev
```

