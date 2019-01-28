from flask_marshmallow import Marshmallow
from marshmallow import fields
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(20), nullable=False, unique=True)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
    
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    
class UserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)

    @classmethod
    def is_token_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class RevokedTokenSchema(ma.Schema):
    id = fields.Integer()
    jti = fields.String(required=True)