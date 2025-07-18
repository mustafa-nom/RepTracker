from flask import Blueprint, request, jsonify
from models import db, Senator

from services.geocodio_api import fetch_reps
import re

reps_bp = Blueprint('representatives', __name__)


@reps_bp.route('/representatives')
def get_current_reps():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400

    data = fetch_reps(zip_code)

    try:
        for result in data.get("results", []): #iterate through the results
            state = result.get("address_components", {}).get("state", "") #get the state
            districts = result.get("fields", {}).get("congressional_districts", []) #get the districts

            for district in districts: #iterate through the districts
                for legislator in district.get("current_legislators", []): #iterate through the legislators
                    if legislator.get("type") == "senator": #check if the legislator is a senator
                        bio = legislator.get("bio", {}) #get the bio
                        full_name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}" #get the full name
                        party = bio.get("party", "")
                        photo_url = bio.get("photo_url", "")

                        # Avoid duplicates
                        existing = Senator.query.filter_by(name=full_name, state=state).first() #check if the senator already exists
                        if not existing:
                            new_senator = Senator(
                                name=full_name,
                                party=party,
                                state=state,
                                photo_url=photo_url
                            )
                            db.session.add(new_senator)

        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to store senators: {str(e)}"}), 500

    # Query all senators in the database
    # Extract only the senators for the current ZIP code from the API response
    senator_list = []
    seen_senator_ids = set()
    for result in data.get("results", []):
        state = result.get("address_components", {}).get("state", "")
        districts = result.get("fields", {}).get("congressional_districts", [])
        for district in districts:
            for legislator in district.get("current_legislators", []):
                if legislator.get("type") == "senator":
                    bio = legislator.get("bio", {})
                    full_name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
                    party = bio.get("party", "")
                    photo_url = bio.get("photo_url", "")

                    if full_name not in seen_senator_ids:
                        seen_senator_ids.add(full_name)
                        senator_list.append({
                            "name": full_name,
                            "party": party,
                            "state": state,
                            "photo_url": photo_url
                        })

    return jsonify({"results": senator_list})
