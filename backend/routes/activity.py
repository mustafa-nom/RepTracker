from flask import Blueprint, request, jsonify
from services.congress_api import fetch_rep_activity
from services.geocodio import fetch_reps

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
    senators_id = []
    congressional_districts = reps["fields"]["congressional_districts"]
    
    # go through each district and get the legislator (in our case its only one district but can be expanded)
    for district in congressional_districts:
        current_legislators = district.get("current_legislators")
        
        # get the current legislators that district
        if current_legislators:
            
            # for each legislator check if they are a senator if they are get their id and append it to the list of ids
            for legislator in current_legislators:
                if legislator["type"] == "senator":
                    references = legislator.get("references")
                    id = references.get("bioguide_id")
                    senators_id.append(id)
    
    # use every id in senators_id and append their activity and jsonify        
    data = []
    for id in senators_id:
        data.append(fetch_rep_activity(id))
    
    return jsonify(data)