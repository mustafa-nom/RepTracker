# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Senator(db.Model):
    __tablename__ = 'senators'

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

class Representative(db.Model):
    __tablename__ = 'representatives'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(255))
    party = db.Column(db.String(50))
    state = db.Column(db.String(10))
    district = db.Column(db.String(10))  # congressional district (cd) number

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "party": self.party,
            "state": self.state,
            "district": self.district
        }

class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    congress = db.Column(db.String(10))
    number = db.Column(db.String(20)) 
    title = db.Column(db.String(512))
    bill_type = db.Column(db.String(10))
    bill_url = db.Column(db.String(255))
    name = db.Column(db.String(100))  # Senator/Rep name who sponsored bill

    def to_dict(self):
        return {
            "id": self.id,
            "congress": self.congress,
            "number": self.number,
            "title": self.title,
            "bill_type": self.bill_type,
            "bill_url": self.bill_url,
            "name": self.name
        }