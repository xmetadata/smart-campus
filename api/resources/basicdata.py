from flask_restful import Resource
from flask_jwt import jwt_required
from common.satree import TreeManager
from common.database import db
from models.basicdata import BasicData
import datetime

class BasicList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm=TreeManager(BasicData, db.session)
        if node_uuid == "root":
            root = BasicData(title="smart school", is_student=False, c_time=datetime.datetime.utcnow())
            tm.add_node(node=root)
            return {"node_uuid" : root.node_uuid}, 200
        else:
            pass

class BasicEdit():
    @jwt_required()
    def post(self, node_uuid):
        pass
    @jwt_required
    def delete(self, node_uuid):
        pass
