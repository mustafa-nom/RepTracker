import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    GEOCODIO_API_KEY=os.getenv('GEOCODIO_API_KEY')
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
    CONGRESS_API_KEY=os.getenv('CONGRESS_API_KEY')