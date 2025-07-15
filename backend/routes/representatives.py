# fetch all reps
from flask import Blueprint, request, jsonify
from services.geocodio import fetch_reps

reps_bp = Blueprint('representatives', __name__)

# return current reps in json format from user zip code
@reps_bp.route('/representatives')
def get_current_reps():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400

    data = fetch_reps(zip_code)
    return jsonify(data)