# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Senator(db.Model):
    __tablename__ = 'senator'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(255))
    party = db.Column(db.String(50))
    state = db.Column(db.String(10))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "party": self.party,
            "state": self.state
        }
