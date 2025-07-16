from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Senator
from routes.representatives import reps_bp
from routes.activity import activity_bp
from routes.summarize import summarize_bp

app = Flask(__name__)
CORS(app)


import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'senators.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# === Register Blueprints ===
app.register_blueprint(reps_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(summarize_bp)

@app.route('/')
def home():
    return {
        "message": "RepTracker works!",
        "endpoints": {
            "representatives": "/representatives?zip=77080",
            "activity": "/activity?zip=ZIPCODE",
            "summarize": "/summarize (POST with JSON body)"
        }
    }

# === Run the App + Create DB Tables ===
if __name__ == '__main__':
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully.")
    app.run(debug=True)
