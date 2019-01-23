from app import db
from bcrypt import gensalt, hashpw, checkpw
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(20), nullable=False)

    def hash_password(self, password):
        self.password = hashpw(password, gensalt())
    

    def check_password(self, password):
        return checkpw(password, self.password)
    
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    
class UserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)
