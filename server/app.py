from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from common.database import db
from common.security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
