from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError
from common.satree import TreeManager
from common.database import db
from models.basicdata import BasicData
import json

class BasicData(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm=TreeManager(BasicData, db.session)
        nodes = tm.find_node(node_uuid=node_uuid, many=True)
        if nodes is None:
            return {"errmsg" : "invalid node_uuid!"}, 400
        else:
            return nodes