from flask import Blueprint, request, jsonify
from services.congress_api import fetch_rep_activity
from services.civic_api import fetch_reps

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activity')
def get_activity():
    # get the rep_id and return data w/ fetch_reps in json format
    # ex: do work
    # data = fetch_reps(rep_id)
    # return jsonify(data) 
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    reps = fetch_reps(zip_code)
    