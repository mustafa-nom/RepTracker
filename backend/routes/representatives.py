from flask import Blueprint, request, jsonify
from services.geocodio_api import fetch_reps
import re

reps_bp = Blueprint('representatives', __name__)

# return current reps in json format from user zip code
@reps_bp.route('/representatives')
def get_current_reps():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400

    data = fetch_reps(zip_code)
    if "error" in data:
        return jsonify(data)
    
    senators = []
    seen_senator_ids = set()
    for district in data["fields"]["congressional_districts"]:
        state_abbr = re.search(r"state:([a-z]{2})", district["ocd_id"], re.I)
        state = state_abbr.group(1).upper() if state_abbr else "??"
        district_num = district['district_number']
        congress_yrs = district['congress_years']
        for legislators in district["current_legislators"]:
            if legislators["type"] != "senator":
                continue
            bid_id = legislators["references"]["bioguide_id"]
            if bid_id in seen_senator_ids:
                continue
            seen_senator_ids.add(bid_id)

            senators.append({
                "bioguide_id": bid_id,
                "name": f"{legislators['bio']['first_name']} {legislators['bio']['last_name']}",
                "party": legislators['bio']['party'],
                "state": state,
                "congress_years": congress_yrs,
                "district_number": district_num,
                "photo": legislators['bio']['photo_url']
            })
    return jsonify(senators) 