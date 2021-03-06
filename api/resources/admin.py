from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError
import json

from common.satree import TreeManager
from common.database import db
from models.nodetree import NodeTree, InNodeSchema

class AdminData(Resource):
    @jwt_required()
    def post(self):
        json_data = json.dumps(request.get_json())
        load_data, errors = InNodeSchema().loads(json_data)
        if errors:
            return errors, 400
        user_data = NodeTree(title=load_data['title'],is_student=load_data['is_student'])
        tm = TreeManager(NodeTree, db.session)
        try:
            if load_data['node_uuid']:
                tm.add_node(load_data['node_uuid'], user_data)
            else:
                tm.add_node(node=user_data)
        except SQLAlchemyError as e:
            return e.message, 500
        return user_data.node_id
