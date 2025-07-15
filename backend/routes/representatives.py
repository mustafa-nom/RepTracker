# fetch all reps
from flask import Blueprint, request, jsonify
<<<<<<< HEAD
from services.geocodio import fetch_reps
=======
from services.geocodio_api import fetch_reps
>>>>>>> c6fb8d59cd7701d140351aba7a8069233272e7ba

reps_bp = Blueprint('representatives', __name__)

# return current reps in json format from user zip code
@reps_bp.route('/representatives')
def get_current_reps():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400

    data = fetch_reps(zip_code)
    return jsonify(data)