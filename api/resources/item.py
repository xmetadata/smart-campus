from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel, UserSchema
from models.item import ItemModel, ItemSchema, ItemOut
from common.message import MSG201, MSG204, MSG403
import json

class ItemList(Resource):
    @jwt_required()
    def get(self, user_id):
        if user_id != current_identity.id:
            return MSG403, 403
        user_detail = UserModel.query.get_or_404(user_id)
        dump_item, errors = ItemSchema(many=True).dump(user_detail.item.all())
        return dump_item, 200

    @jwt_required()
    def post(self, user_id):
        if user_id != current_identity.id:
            return MSG403, 403
        json_data = json.dumps(request.get_json())
        user_detail = UserModel.query.get_or_404(user_id)
        try:
            load_data, errors = ItemOut().loads(json_data)
            if errors:
                return errors, 400
            new_item = ItemModel(load_data['name'], load_data['price'], user_detail.id)
            new_item.add(new_item)
        except SQLAlchemyError as e:
            return e.message, 500
        return ItemSchema().dump(new_item), 201

class ItemDetail(Resource):
    @jwt_required()
    def get(self, user_id, id):
        if user_id != current_identity.id:
            return MSG403, 403
        user_detail = UserModel.query.get_or_404(user_id)
        item_detail = ItemModel.query.get_or_404(id)
        item_dump, errors = ItemSchema().dump(item_detail)
        return item_dump, 200

    @jwt_required()
    def delete(self, user_id, id):
        if user_id != current_identity.id:
            return MSG403, 403
        user_detail = UserModel.query.get_or_404(user_id)
        item_detail = ItemModel.query.get_or_404(id)
        try:
            item_detail.delete(item_detail)
        except SQLAlchemyError as e:
            return e.message, 500
        return MSG204, 204
