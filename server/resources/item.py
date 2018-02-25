from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required
from models.item import ItemModel

# input filter
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
# output filter
resource_fields = {
    'name': fields.String,
    'uri': fields.Url('item')
}


# /item/<string:name>/
class Item(Resource):
    @jwt_required()
    @marshal_with(resource_fields, envelope='resource')
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        result, message = item.delete(item)
        if result:
            return message, 204
        else:
            return message, 401

    def put(self, name):
        data = parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        result, message = item.update()
        if result:
            return message, 204
        else:
            return message, 401


# /item/
class ItemList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        return ItemModel.query.all()

    def post(self):
        data = parser.parse_args()
        item = ItemModel(data['name'], data['price'])
        result, message = item.add(item)
        if result:
            return message, 201
        else:
            return message, 401
