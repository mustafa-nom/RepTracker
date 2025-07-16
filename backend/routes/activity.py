from flask import Blueprint, request, jsonify
from services.congress_api import fetch_rep_activity
from services.geocodio_api import fetch_reps

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activity')
def get_activity():
    # TODO get photo URL for all the senators
    # TODO make the data cleaner
    
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    
    reps = fetch_reps(zip_code)
    bills = []
    congressional_districts = reps["fields"]["congressional_districts"]
    
    # go through each district and get the legislator (in our case its only one district but can be expanded)
    for district in congressional_districts:
        current_legislators = district.get("current_legislators")
        
        # get the current legislators that district
        if current_legislators:
            
            # for each legislator check if they are a senator if they are get their id and append it to the list of ids
            for legislator in current_legislators:
                if legislator["type"] == "senator":
                    # Saves the name of the legislator
                    name = f"{legislator["bio"]["first_name"]} {legislator["bio"]["last_name"]}"
                    
                    # Gets the id so we can use it for fetching the activity of the bill
                    references = legislator.get("references")
                    id = references.get("bioguide_id")
                    
                    # Gets the bills
                    sponsored_legislation = fetch_rep_activity(id)
                    legislation_array = sponsored_legislation["sponsoredLegislation"]
                
                    # Append the name and bills. The bills array will hold a dictionary of the name and bills of each senator.
                    bills.append({
                        "name": name,
                        "bills": legislation_array,
                    })
                    
    
    # use every id in senators_id and append their activity and jsonify        
    # data = []
    # for id in senators_id:
    #     data.append(fetch_rep_activity(id))
    
    return jsonify(bills)