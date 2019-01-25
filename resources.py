from app import db
from flask import request
from flask_restful import Resource


from models import User, UserSchema


users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'status': 'error', 'message': 'No input received'}, 400
        
        data, errors = user_schema.load(json_data)
        if errors:
            return {'status': 'error', 'errors': errors}, 422

        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'status': 'error', 'message':'Username already in use'}, 400

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'status': 'error', 'message':'Email already in use'}, 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=User.hash_password(data['password'])
        )
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return {'status': 'success', 'data': result}, 200

