from flask import Blueprint, request, jsonify, render_template_string
from models import Senator

senators_bp = Blueprint('senators', __name__)

@senators_bp.route('/senator/photo/view')
def view_senator_photo():
    name = request.args.get('name')
    if not name:
        return "Missing senator name", 400

    senator = Senator.query.filter_by(name=name).first()
    if not senator:
        return "Senator not found", 404


    return render_template_string(f"""
        <html>
            <head><title>{senator.name} - Photo</title></head>
            <body style="text-align: center; font-family: Arial;">
                <h2>{senator.name} ({senator.party})</h2>
                <p>{senator.state}</p>
                <img src="{senator.photo_url}" alt="Senator Photo" style="max-height: 500px;" />
            </body>
        </html>
    """)