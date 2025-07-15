from flask import Blueprint, request, jsonify
from services.gemini_api import summarize_text

summarize_bp = Blueprint('summarize', __name__)

# summarize everything