from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from common.database import db
from common.schema import ma
from common.security import authenticate, identity, payload_handle, auth_url_rule, auth_url_options
from resources.register import Register
from resources.admin import AdminData
from resources.nodetree import TreeRoot, TreeList, TreeEdit

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
ma.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)
jwt.jwt_payload_handler(payload_handle)
app.add_url_rule(auth_url_rule, **auth_url_options)

api.add_resource(AdminData, '/admin')
api.add_resource(Register, '/register')
#tree root
api.add_resource(TreeRoot, '/noderoot')
#tree list
api.add_resource(TreeList, '/nodetree/<string:node_uuid>')
#tree edit
api.add_resource(TreeEdit, '/node/<string:node_uuid>')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
