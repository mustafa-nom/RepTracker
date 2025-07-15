from flask import Blueprint, request, jsonify
from services.gemini_api import summarize_text

summarize_bp = Blueprint('summarize', __name__)
@summarize_bp.route('/summarize', methods=['POST'])
def summarize_endpoint():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "missing text field"}), 400
    
    text = data['text']
    summary = summarize_text(text)
    return jsonify({"summary": summary})