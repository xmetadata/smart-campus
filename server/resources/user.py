from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists."}, 400

        user = UserModel(data['username'], data['password'])
        result, message = user.add(user)
        if result:
            return message, 201
        else:
            return message, 401
