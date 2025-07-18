from flask import Blueprint, request, jsonify
from services.congress_api import fetch_rep_activity, get_bill_summary
from services.geocodio_api import fetch_reps
from models2 import db, Bill
activity_bp = Blueprint('activity', __name__)
@activity_bp.route('/activity')
def get_activity():

    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({"error": "missing zip code"}), 400
    reps = fetch_reps(zip_code)
    bills = []
    try: 
        congressional_districts = reps["results"][0]["fields"]["congressional_districts"]
    except IndexError:
        return jsonify({"error": "congressional_districts DNE"})

    
    # go through each district and get the legislator (in our case its only one district but can be expanded)
    for district in congressional_districts:
        current_legislators = district.get("current_legislators")
        # get the current legislators that district
        if current_legislators:
            # for each legislator check if they are a senator if they are get their id and append it to the list of ids
            for legislator in current_legislators:
                if legislator["type"] == "senator":
                    # Saves the name of the legislator
                    name = f"{legislator['bio']['first_name']} {legislator['bio']['last_name']}"
                    # Gets the id so we can use it for fetching the activity of the bill
                    references = legislator.get("references")
                    id = references.get("bioguide_id")
                    # Gets the bills
                    sponsored_legislation = fetch_rep_activity(id)
                    if not sponsored_legislation or "sponsoredLegislation" not in sponsored_legislation:
                        print(f"[WARN] Missing sponsoredLegislation for {name} (ID: {id})")
                        continue

                    legislation_array = sponsored_legislation["sponsoredLegislation"]
                    for bill in legislation_array:
                        if not isinstance(bill, dict) or not all(k in bill for k in ["congress", "number", "type"]):
                            print(f"[SKIP] Malformed bill for {name}: {bill}")
                            continue

                        congress = bill["congress"]
                        bill_id = bill["number"]
                        bill_type = bill["type"]

                        summary_data = get_bill_summary(congress, bill_type, bill_id)
                        summary_text = "No summary available."
                        if summary_data and "summaries" in summary_data and summary_data["summaries"]:
                            summary_text = summary_data["summaries"][0].get("text", summary_text)

                        bill["summary"] = summary_text
                    if not Bill.query.filter_by(number=bill_id, congress=congress, name=name).first():
                        new_bill = Bill(
                            congress=congress,
                            number=bill_id,
                            title=bill.get("title"),
                            bill_type=bill_type,
                            bill_url=bill.get("url"),
                            name=name
                        )
                        db.session.add(new_bill)

                    bills.append({
                        "name": name,
                        "bills": legislation_array,
                    })

    # use every id in senators_id and append their activity and jsonify
    # data = []
    # for id in senators_id:
    #     data.append(fetch_rep_activity(id))
    db.session.commit()

    return jsonify(bills)