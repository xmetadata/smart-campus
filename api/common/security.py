from flask_restful import request
from flask.globals import current_app
from flask_jwt import _jwt, JWTError
from sqlalchemy.exc import SQLAlchemyError
from models.admin import Admin, LoginSchema
import datetime
import json

def authenticate(username, password, user_type):
    try:
        user = Admin.find_by_phone_number(username)
    except SQLAlchemyError as e:
        return
    if user and user.confirm_password(password):
        if user_type == 'wechat' and user.role == 1:
            return user
        elif user_type == 'local' and user.role != 1:
            return user

def identity(payload):
    uuid = payload['identity']
    return Admin.find_by_uuid(uuid)

def payload_handle(identity):
    iat = datetime.datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, 'uuid') or identity['uuid']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

def auth_request_handle():
    data = request.get_json()
    username    = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    password    = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
    user_type   = data.get('user_type', None)
    criterion = [username, password, user_type, len(data) == 3]

    if not all(criterion):
        raise JWTError('Bad Request', 'Invalid credentials')

    identity = _jwt.authentication_callback(username, password, user_type)

    if identity:
        access_token = _jwt.jwt_encode_callback(identity)
        return _jwt.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials')

auth_url_rule='/auth'
auth_url_options = {'methods': ['POST'],'view_func':auth_request_handle}
