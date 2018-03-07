from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from models.user import UserModel, UserSchema
from models.item import ItemModel, ItemSchema
from sqlalchemy.exc import SQLAlchemyError
from common.message import MSG201, MSG403

class UserList(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            load_data, errors = UserSchema().load(json_data)
            if errors:
                return errors, 400
            new_user = UserModel(load_data['username'], load_data['password'])
            new_user.add(new_user)
        except SQLAlchemyError as e:
            return e.message, 500
        return MSG201, 201

class UserDetail(Resource):
    @jwt_required()
    def get(self, id):
        if id != current_identity.id:
            return MSG403, 403
        user_detail = UserModel.query.get_or_404(id)
        dump_user, errors = UserSchema().dump(user_detail)
        dump_item, errors = ItemSchema(many=True, exclude=('user',)).dump(user_detail.item.all())
        return {'user': dump_user, 'item': dump_item}, 200
