from flask import Blueprint, request, jsonify, render_template_string
from models import db, Senator
from markupsafe import Markup, escape

senators_bp = Blueprint('senators', __name__)

@senators_bp.route('/senator/photo/view')
def view_senator_photo():
    name = request.args.get('name')
    if not name:
        return "Missing senator name", 400

    senator = Senator.query.filter_by(name=name).first()
    if not senator:
        return "Senator not found", 404

    # Safe template rendering with escaped variables
    template = """
        <html>
            <head><title>{{ name }} - Photo</title></head>
            <body style="text-align: center; font-family: Arial;">
                <h2>{{ name }} ({{ party }})</h2>
                <p>{{ state }}</p>
                <img src="{{ photo_url }}" alt="Senator Photo" style="max-height: 500px;" />
            </body>
        </html>
    """
    
    return render_template_string(template, 
                                  name=senator.name,
                                  party=senator.party,
                                  state=senator.state,
                                  photo_url=senator.photo_url)