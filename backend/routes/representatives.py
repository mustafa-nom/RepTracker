from flask import Blueprint, request, jsonify
from models import db, Senator

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

    try:
        for result in data.get("results", []):
            state = result.get("address_components", {}).get("state", "")
            districts = result.get("fields", {}).get("congressional_districts", [])

            for district in districts:
                for legislator in district.get("current_legislators", []):
                    if legislator.get("type") == "senator":
                        bio = legislator.get("bio", {})
                        full_name = f"{bio.get('first_name', '')} + " + f"{bio.get('last_name', '')}"
                        poltical_party = bio.get("party", "")
                        photo_url = bio.get("photo_url", "")

                        # Avoid duplicates
                        existing = Senator.query.filter_by(name=full_name, state=state).first()
                        if not existing:
                            new_senator = Senator(
                                name=full_name,
                                party=political_party,
                                state=state,
                                photo_url=photo_url
                            )
                            db.session.add(new_senator)

        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to store senators: {str(e)}"}), 500

    return jsonify(data)
