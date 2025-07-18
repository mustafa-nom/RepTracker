from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    congress = db.Column(db.String(10))
    number = db.Column(db.String(20)) 
    title = db.Column(db.String(512))
    bill_type = db.Column(db.String(10))
    bill_url = db.Column(db.String(255))
    name = db.Column(db.String(100))

    def to_dict(self):
        return {
            "congress": self.congress,
            "number": self.number,
            "title": self.title,
            "bill_type": self.bill_type,
            "bill_url": self.bill_url,
            "name": self.name
        }
