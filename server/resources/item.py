from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required
from models.item import ItemModel

resource_fields = {
    'name': fields.String,
    'uri': fields.Url('item')
}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!'
                        )

    @jwt_required()
    @marshal_with(resource_fields, envelope='resource')
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item.delete(item):
            return item, 204
        else:
            return {'message': 'SQLAlchemyError'}, 401

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        if item.delete(item):
            return item, 204
        else:
            return {'message': 'SQLAlchemyError'}, 401


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!'
                        )

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        return ItemModel.query.all()

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        data = self.parser.parse_args()
        item = ItemModel(data['name'], data['price'])
        if item.add(item):
            return item, 201
        else:
            return {'message': 'SQLAlchemyError'}, 401
