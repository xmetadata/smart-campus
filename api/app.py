from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from common.database import db
from common.schema import ma
from common.security import authenticate, identity, payload_handle, auth_url_rule, auth_url_options
from resources.item import ItemList, ItemDetail
from resources.user import UserList, UserDetail
from resources.register import Register
from resources.admin import AdminData
from resources.basicdata import BasicData

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
ma.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)
jwt.jwt_payload_handler(payload_handle)
app.add_url_rule(auth_url_rule, **auth_url_options)


api.add_resource(ItemDetail, '/user/<int:user_id>/item/<int:id>')
api.add_resource(ItemList, '/user/<int:user_id>/item')
api.add_resource(UserList, '/user')
api.add_resource(UserDetail, '/user/<int:id>')
api.add_resource(AdminData, '/admin')
api.add_resource(Register, '/register')
api.add_resource(BasicData, '/BasicList/<string:node_uuid>')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
