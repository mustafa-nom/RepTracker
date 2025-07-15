from flask import Flask
from routes.representatives import reps_bp
from flask_cors import CORS
from routes.activity import activity_bp
from routes.summarize import summarize_bp

app = Flask(__name__)
CORS(app)
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
    
if __name__ == '__main__':
    app.run(debug=True)