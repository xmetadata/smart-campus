from flask_restful import Resource, request
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from common.satree import TreeManager
from common.database import db
from models.basicdata import BasicData, ListSchema, BasicEditSchema
import datetime
import json

class BasicList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm=TreeManager(BasicData, db.session)
        basic_node = None
        if node_uuid == "root":
            root = tm.get_root_node()
            if root is None:
                root = BasicData(title="smart school", is_student=False, c_time=datetime.datetime.utcnow())
                tm.add_node(node=root)
                return {"title" : root.title, "node_uuid" : root.node_uuid}, 200
            basic_node = root
        else:
            basic_node = tm.find_node(node_uuid=node_uuid)
        nodes = tm.find_node(node_uuid=basic_node.node_uuid, many=True)
        return {"title" : basic_node.title, "node_uuid" : basic_node.node_uuid, "children" : ListSchema(many=True).dump(nodes).data}, 200

class BasicEdit(Resource):
    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(BasicData, db.session)
        req_data = json.dumps(request.get_json())
        load_data, errors = BasicEditSchema().loads(req_data)
        if errors:
            return errors, 400
        basic_node = tm.find_node(node_uuid=node_uuid)
        if basic_node is None:
            return {"msg" : "invalid node_uuid"}, 400
        if load_data['action'] == 'add':
            node = BasicData(title=load_data['node']['title'], is_student=load_data['node']['is_student'])
            try:
                tm.add_node(node_uuid=basic_node.node_uuid, node=node)
            except SQLAlchemyError as e:
                return {'msg': e.message}, 400
            return {'msg' : 'add success'}, 200
        elif load_data['action'] ==  'update':
            basic_node.title = load_data['node']['title']
            tm.update_node(basic_node)
            return {'msg' : 'update success'}, 200
        else:
            return {'msg' : 'invalid action'}, 400

    @jwt_required
    def delete(self, node_uuid):
        tm = TreeManager(BasicData, db.session)
        try:
            basic_node = tm.find_node(node_uuid=node_uuid)
        except SQLAlchemyError as e:
            return {'msg' : e.message}, 400
        if basic_node is None:
            return {'msg' : 'invalid node_uuid'}, 400
        tm.delete_node(node_uuid)
        return {'msg' : 'delete success'}, 200
