from app import db
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)


from models import (
    User,
    UserSchema,
    RevokedToken,
    RevokedTokenSchema)


users_schema = UserSchema(many=True)
user_schema = UserSchema()

tokens_schema = RevokedTokenSchema(many=True)
token_schema = RevokedTokenSchema()

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


class UserLogin(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'status': 'error', 'message': 'No input received'}, 400

        data, errors = user_schema.load(json_data,partial=True)
        if errors:
            return {'status': 'error', 'errors': errors}

        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'status': 'error', 'message': 'Invalid username/password'}, 400
        
        if not User.check_password(user.password, data['password']):
            return {'status': 'error', 'message': 'Invalid username/password'}, 400
        
        user = user_schema.dump(user).data

        access_token = create_access_token(identity=data['email'])

        return {'status': 'success', 'data': {
            'username': user["username"],
            'email': user["email"]
        }}, 200, {"Authorization": access_token}


class LogoutAccessToken(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {'status': 'success', 'message': 'Access token revoked'}                

