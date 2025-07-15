import os

class Config:
    CIVIC_API_KEY=os.getenv('CIVIC_API_KEY')
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
    # add sqlite or diff db