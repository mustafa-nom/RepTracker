from flask import Blueprint, request, jsonify
from services.congress_api import fetch_rep_activity, get_bill_summary, get_bill_details
from services.geocodio_api import fetch_reps
from models import db, Bill
from functools import lru_cache
import logging

activity_bp = Blueprint('activity', __name__)
logger = logging.getLogger(__name__)


'''
Added caching because activity was taking too long
This will remove any entry that hasnt been used in a while and replace it
'''
@lru_cache(maxsize=1000)
def cached_bill_summary(congress, bill_type, bill_number):
    """Cache bill summaries to reduce API calls"""
    return get_bill_summary(congress, bill_type, bill_number)


def process_legislator(legislator, max_bills=5, offset=0):
    """Process a single legislator's bills with a limit"""
    legislator_type = legislator.get("type", "")
    bio = legislator.get("bio", {})
    name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
    references = legislator.get("references", {})
    bioguide_id = references.get("bioguide_id")
    
    if not bioguide_id:
        logger.warning(f"No bioguide_id for {name}")
        return None
    
    try:
        sponsored_legislation = fetch_rep_activity(bioguide_id)

        if isinstance(sponsored_legislation, dict) and "error" in sponsored_legislation:
            logger.error(f"API error for {name}: {sponsored_legislation['error']}")
            return None
        if not sponsored_legislation or "sponsoredLegislation" not in sponsored_legislation:
            logger.warning(f"No sponsored legislation found for {name} (ID: {bioguide_id})")
            return None
        
        legislation_array = sponsored_legislation.get("sponsoredLegislation", [])
        legislator_bills = []
        bills_processed = 0
        bills_failed = 0
        
        # get bills w/ offset + limit
        bills_to_process = legislation_array[offset:offset + max_bills]
        
        for bill in bills_to_process:
            try:
                if not isinstance(bill, dict):
                    logger.warning(f"Invalid bill format for {name}: {bill}")
                    bills_failed += 1
                    continue
                
                # skip amendments for now since its diff than bill --> come back if needed
                if 'amendmentNumber' in bill and 'number' not in bill:
                    continue
                
                congress = bill.get("congress")
                bill_number = bill.get("number")
                bill_type = bill.get("type")
                
                if not all([congress, bill_number, bill_type]):
                    logger.warning(f"Missing required fields for bill: {bill}")
                    bills_failed += 1
                    continue
                
                # if bill exists --> use cached data, else get summary
                existing_bill = Bill.query.filter_by(
                    number=str(bill_number), 
                    congress=str(congress), 
                    name=name
                ).first()
                
                if existing_bill:
                    bill["summary"] = "Previously cached - check database"
                else:
                    # Checks the cache for the bill
                    summary_text = "No summary available."
                    try:
                        summary_data = cached_bill_summary(congress, bill_type, bill_number)
                        if isinstance(summary_data, dict) and "error" in summary_data:
                            logger.error(f"Summary API error for bill {bill_number}: {summary_data['error']}")
                        elif summary_data and "summaries" in summary_data and summary_data["summaries"]:
                            summary_text = summary_data["summaries"][0].get("text", "No summary available.")
                    except Exception as e:
                        logger.error(f"Failed to get summary for bill {bill_number}: {str(e)}")
                    
                
                    bill["summary"] = summary_text
                    
                    # Get the bill data
                    try:
                        bill_details = get_bill_details(congress, bill_type, bill_number)
                        if isinstance(bill_details, dict) and "error" not in bill_details:
                            bill["introducedDate"] = bill_details.get("introducedDate")
                            bill["latestAction"] = bill_details.get("latestAction")
                            bill["policyArea"] = bill_details.get("policyArea")
                    except Exception as e:
                        logger.error(f"Failed to get bill details for {bill_number}: {str(e)}")
                    
                    # Make a bill object with the given data and put it in the database and increase the size of the bills processes
                    try:
                        new_bill = Bill(
                            congress=str(congress),
                            number=str(bill_number),
                            title=bill.get("title", ""),
                            bill_type=bill_type,
                            bill_url=bill.get("url", ""),
                            name=name
                        )
                        db.session.add(new_bill)
                        db.session.commit()
                    except Exception as db_error:
                        db.session.rollback()
                        logger.error(f"Database error saving bill {bill_number}: {str(db_error)}")
                        bills_failed += 1
                        continue
                
                legislator_bills.append(bill)
                bills_processed += 1
                
            except Exception as bill_error:
                logger.error(f"Error processing bill for {name}: {str(bill_error)}")
                bills_failed += 1
                continue
        
        if legislator_bills:
            result = {
                "name": name,
                "type": legislator_type,
                "bioguide_id": bioguide_id,
                "bills": legislator_bills,
                "offset": offset + len(legislator_bills),
                "has_more": offset + len(legislator_bills) < len(legislation_array),
                "total_bills": len(legislation_array),
                "bills_shown": len(legislator_bills),
                "bills_processed": bills_processed,
                "bills_failed": bills_failed
            }
            
            if bills_failed > 0:
                result["warning"] = f"{bills_failed} bills could not be processed"
                
            return result
            
    except Exception as e:
        logger.error(f"Failed to process legislator {name}: {str(e)}")
        return {
            "name": name,
            "type": legislator_type,
            "bioguide_id": bioguide_id,
            "error": f"Failed to fetch legislation: {str(e)}",
            "bills": []
        }
    
    return None

@activity_bp.route('/activity')
def get_activity():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    
    # optional parameter for max bills per legislator --> may use for infiite scrolling
    max_bills = request.args.get('max_bills', 5, type=int)
    
    # fetch representatives data
    reps = fetch_reps(zip_code)
    
    if isinstance(reps, dict) and "error" in reps:
        return jsonify(reps), 400
    
    try: 
        results = reps.get("results", [])
        if not results:
            return jsonify({"error": "No results found for this zip code"}), 404
            
        congressional_districts = results[0].get("fields", {}).get("congressional_districts", [])
        if not congressional_districts:
            return jsonify({"error": "No congressional districts found for this zip code"}), 404
    except (IndexError, KeyError, TypeError) as e:
        return jsonify({"error": f"Error parsing response: {str(e)}"}), 500

    all_legislators = []
    seen_names = set()  
    
    for district in congressional_districts:
        current_legislators = district.get("current_legislators", [])
        for legislator in current_legislators:
            bio = legislator.get("bio", {})
            name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
            
            if name not in seen_names:
                seen_names.add(name)
                all_legislators.append(legislator)
    
    bills_response = []
    legislators_processed = 0
    legislators_failed = 0
    
    for legislator in all_legislators:
        try:
            result = process_legislator(legislator, max_bills)
            if result:
                if "error" in result:
                    legislators_failed += 1
                else:
                    legislators_processed += 1
                bills_response.append(result)
        except Exception as e:
            logger.error(f"Failed to process legislator: {str(e)}")
            legislators_failed += 1
            continue
    
    response_data = {
        "legislators": bills_response,
        "total_legislators": len(bills_response),
        "legislators_processed": legislators_processed,
        "legislators_failed": legislators_failed,
        "max_bills_per_legislator": max_bills
    }
    
    # check if some legislators failed
    if legislators_failed > 0:
        response_data["warning"] = f"{legislators_failed} legislators could not be processed"
    
    return jsonify(response_data)

# might use this route for giving cached data everytime someone has been prev fetched -- TBD so ignore
@activity_bp.route('/activity/quick')
def get_activity_quick():
    """Quick endpoint that returns cached data only"""
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    
    reps = fetch_reps(zip_code)
    
    if isinstance(reps, dict) and "error" in reps:
        return jsonify(reps), 400
    try:
        results = reps.get("results", [])
        if not results:
            return jsonify({"error": "No results found for this zip code"}), 404
        
        legislators_info = []
        seen_names = set()
        congressional_districts = results[0].get("fields", {}).get("congressional_districts", [])
        
        for district in congressional_districts:
            for legislator in district.get("current_legislators", []):
                bio = legislator.get("bio", {})
                name = f"{bio.get('first_name', '')} {bio.get('last_name', '')}"
                
                if name in seen_names:
                    continue
                seen_names.add(name)
                
                legislator_type = legislator.get("type", "")
                try:
                    cached_bills = Bill.query.filter_by(name=name).limit(5).all()
                    if cached_bills:
                        legislators_info.append({
                            "name": name,
                            "type": legislator_type,
                            "cached_bills": [bill.to_dict() for bill in cached_bills],
                            "source": "cache"
                        })
                except Exception as db_error:
                    logger.error(f"Database error fetching cached bills for {name}: {str(db_error)}")
                    legislators_info.append({
                        "name": name,
                        "type": legislator_type,
                        "cached_bills": [],
                        "source": "cache",
                        "error": "Failed to fetch cached bills"
                    })
        
        return jsonify({
            "legislators": legislators_info,
            "note": "This is cached data only. Use /activity for fresh data."
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@activity_bp.route('/activity/legislator/<bioguide_id>')
def get_legislator_bills(bioguide_id):
    """Get bills for a specific legislator with pagination"""
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 5, type=int)
    
    # limit max bills per request to prevent abuse
    limit = min(limit, 20)
    
    try:
        sponsored_legislation = fetch_rep_activity(bioguide_id)

        if isinstance(sponsored_legislation, dict) and "error" in sponsored_legislation:
            return jsonify(sponsored_legislation), 404
        
        if not sponsored_legislation or "sponsoredLegislation" not in sponsored_legislation:
            return jsonify({"error": "No sponsored legislation found"}), 404
        
        legislation_array = sponsored_legislation.get("sponsoredLegislation", [])
        bills_to_process = legislation_array[offset:offset + limit]
        
        processed_bills = []
        bills_failed = 0
        
        for bill in bills_to_process:
            try:
                if not isinstance(bill, dict):
                    bills_failed += 1
                    continue
                
                # skip amendments for now
                if 'amendmentNumber' in bill and 'number' not in bill:
                    continue
                
                congress = bill.get("congress")
                bill_number = bill.get("number")
                bill_type = bill.get("type")
                
                if not all([congress, bill_number, bill_type]):
                    bills_failed += 1
                    continue
                
                summary_text = "No summary available."
                try:
                    summary_data = cached_bill_summary(congress, bill_type, bill_number)
                    if isinstance(summary_data, dict) and "error" not in summary_data:
                        if summary_data and "summaries" in summary_data and summary_data["summaries"]:
                            summary_text = summary_data["summaries"][0].get("text", "No summary available.")
                except Exception as e:
                    logger.error(f"Failed to get summary for bill {bill_number}: {str(e)}")
                bill["summary"] = summary_text
                
                try:
                    bill_details = get_bill_details(congress, bill_type, bill_number)
                    if isinstance(bill_details, dict) and "error" not in bill_details:
                        bill["introducedDate"] = bill_details.get("introducedDate")
                        bill["latestAction"] = bill_details.get("latestAction")
                        bill["policyArea"] = bill_details.get("policyArea")
                except Exception as e:
                    logger.error(f"Failed to get bill details for {bill_number}: {str(e)}")
                    
                processed_bills.append(bill)
            except Exception as e:
                logger.error(f"Error processing bill: {str(e)}")
                bills_failed += 1
                continue
        
        response_data = {
            "bioguide_id": bioguide_id,
            "bills": processed_bills,
            "offset": offset + len(processed_bills),
            "has_more": offset + len(processed_bills) < len(legislation_array),
            "total_bills": len(legislation_array)
        }
        
        if bills_failed > 0:
            response_data["warning"] = f"{bills_failed} bills could not be processed"
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch bills: {str(e)}"}), 500