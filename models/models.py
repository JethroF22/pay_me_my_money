from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(20), nullable=False)
