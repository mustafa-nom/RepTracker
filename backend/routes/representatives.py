from flask import Blueprint, request, jsonify
from models import db, Senator, Representative
from services.geocodio_api import fetch_reps
import re

reps_bp = Blueprint('representatives', __name__)

@reps_bp.route('/representatives')
def get_current_reps():
    """Get all representatives (both senators and house members) for a zip code"""
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    
    data = fetch_reps(zip_code)
    if isinstance(data, dict) and "error" in data:
        return jsonify(data), 400
    
    senators = []
    house_members = []
    seen_legislators = set() 
    
    try:
        for result in data.get("results", []):
            state = result.get("address_components", {}).get("state", "")
            districts = result.get("fields", {}).get("congressional_districts", [])
            
            for district in districts:
                district_number = district.get("district_number", "")
                
                for legislator in district.get("current_legislators", []):
                    bio = legislator.get("bio", {})
                    full_name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
                    party = bio.get("party", "")
                    photo_url = bio.get("photo_url", "")
                    legislator_type = legislator.get("type", "")
                    
                    # unique key to avoid duplicates
                    unique_key = f"{full_name}-{state}-{legislator_type}"
                    
                    if unique_key not in seen_legislators:
                        seen_legislators.add(unique_key)
                        
                        legislator_info = {
                            "name": full_name,
                            "party": party,
                            "state": state,
                            "photo_url": photo_url,
                            "type": legislator_type
                        }
                        
                        if legislator_type == "senator": # add to db if senator, else add rep
                            existing = Senator.query.filter_by(name=full_name, state=state).first()
                            if not existing:
                                new_senator = Senator(
                                    name=full_name,
                                    party=party,
                                    state=state,
                                    photo_url=photo_url
                                )
                                db.session.add(new_senator)
                            
                            senators.append(legislator_info)
                            
                        elif legislator_type == "representative":
                            legislator_info["district"] = district_number
                            existing = Representative.query.filter_by(
                                name=full_name, 
                                state=state,
                                district=str(district_number)
                            ).first()
                            
                            if not existing:
                                new_representative = Representative(
                                    name=full_name,
                                    party=party,
                                    state=state,
                                    photo_url=photo_url,
                                    district=str(district_number)
                                )
                                db.session.add(new_representative)
                            
                            house_members.append(legislator_info)
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to process representatives: {str(e)}"}), 500
    
    # returns both senators & rep + local count
    return jsonify({
        "senators": senators,
        "representatives": house_members,
        "total_count": len(senators) + len(house_members)
    })

@reps_bp.route('/representatives/<rep_type>')
def get_reps_by_type(rep_type):
    """Get only senators or only representatives for a zip code"""
    if rep_type not in ['senators', 'representatives']:
        return jsonify({"error": "Invalid type. Use 'senators' or 'representatives'"}), 400
    
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    
    data = fetch_reps(zip_code)
    if isinstance(data, dict) and "error" in data:
        return jsonify(data), 400
    
    results = []
    seen_legislators = set()
    
    try:
        for result in data.get("results", []):
            state = result.get("address_components", {}).get("state", "")
            districts = result.get("fields", {}).get("congressional_districts", [])
            
            for district in districts:
                district_number = district.get("district_number", "")
                
                for legislator in district.get("current_legislators", []):
                    bio = legislator.get("bio", {})
                    full_name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
                    party = bio.get("party", "")
                    photo_url = bio.get("photo_url", "")
                    legislator_type = legislator.get("type", "")
                    
                    unique_key = f"{full_name}-{state}-{legislator_type}"
                    
                    if unique_key not in seen_legislators:
                        seen_legislators.add(unique_key)
                        
                        if (rep_type == 'senators' and legislator_type == 'senator') or \
                           (rep_type == 'representatives' and legislator_type == 'representative'):
                            
                            legislator_info = {
                                "name": full_name,
                                "party": party,
                                "state": state,
                                "photo_url": photo_url,
                                "type": legislator_type
                            }
                            
                            if legislator_type == "representative":
                                legislator_info["district"] = district_number
                            
                            results.append(legislator_info)
        
        return jsonify({
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to process {rep_type}: {str(e)}"}), 500