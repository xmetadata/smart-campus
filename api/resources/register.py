from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from models.admin import Admin, LoginSchema, AdminTestSchema
from sqlalchemy.exc import SQLAlchemyError
import json

class Register(Resource):
    def post(self):
        req_json = json.dumps(request.get_json())
        print "@@@@@@@@@@@@@@@@@@@@"
        print req_json
        try:
            load_data, errors = LoginSchema().loads(req_json)
            if errors:
                return errors, 400
            new_user = Admin(phone_number=load_data['phone_number'], password=load_data['password'], role= 1 if load_data['user_type'] == 'wechat' else 2)
            new_user.add(new_user)
        except SQLAlchemyError as e:
            return e.message, 500
        return AdminTestSchema().dump(new_user), 201

