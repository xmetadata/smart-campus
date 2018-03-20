from flask_restful import Resource, request
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from common.satree import TreeManager
from common.database import db
from common.retmsg import ret_msg
from models.nodetree import NodeTree, ListSchema, InNodeSchema, OutNodeSchema
from models.admin import Admin
import json
import uuid

class TreeRoot(Resource):
    @jwt_required()
    def get(self):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="create manager tree failed.")
        else:
            root = tm.get_root_node()
            if root is None:
                return ret_msg(status=False, msg="can't find root node.")
            else:
                return ret_msg(status=True, msg="find root success", data=ListSchema().dump(root).data)
    @jwt_required()
    def post(self):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="create manager tree failed.")
        else:
            req_json = json.dumps(request.get_json())
            load_data, errors = InNodeSchema(exclude=('patriarch')).loads(req_json)
            if errors:
                return ret_msg(status=False, msg="parse request data failed.")
            root = NodeTree(title=load_data['title'], is_student=load_data['is_student'])
            status, error = tm.add_node(node=root)
            if status:
                return ret_msg(status=True, msg="add root node success.")
            else:
                return ret_msg(status=False, msg=error)

class TreeList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        status, data = tm.find_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=data)
        status, nodes = tm.find_node(node_uuid=data.node_uuid, many=True)
        if status is False:
            return ret_msg(status=False, msg=nodes)
        ret_data = {"title" : data.title, "node_uuid" : data.node_uuid, "children" : ""}
        ret_data['children'] = OutNodeSchema(many=True).dump(nodes).data
        return ret_msg(status=True, msg="find success", data=ret_data)

class TreeEdit(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        status, node = tm.find_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=node)
        return ret_msg(status=True, msg="find node success", data=OutNodeSchema().dump(node).data)
    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        status, basic_node = tm.find_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=basic_node)
        req_json = json.dumps(request.get_json())
        load_data, errors = InNodeSchema().loads(req_json)
        if errors:
            return ret_msg(status=False, msg="parse request data failed.")
        new_node = NodeTree(title=load_data['title'], is_student=load_data['is_student'])
        if load_data['is_student']:
            user_set = []
            patriarch_list = json.loads(json.dumps(load_data['patriarch']))
            for ite in patriarch_list:
                    user_set.append(Admin(phone_number=ite, password=ite[-4:], uuid=uuid.uuid1(), nodes=[new_node, ]))
            new_node.users = user_set
        status, error = tm.add_node(node_uuid=node_uuid, node=new_node)
        if status is False:
            return ret_msg(status=False, msg=error)
        return ret_msg(status=True, msg="add success")

    @jwt_required()
    def put(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        req_json = json.dumps(request.get_json())
        load_data, errors = InNodeSchema().loads(req_json)
        if errors:
            return ret_msg(status=False, msg="parse request data failed.")
        status, node = tm.find_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=node)
        node.title = load_data['title']
        if load_data['is_student']:
            status, nodes = Admin().find_node_by_uuid(node.node_uuid)
            if status is False:
                return ret_msg(status=False, msg=nodes)
            elif nodes is None:
                return ret_msg(status=False, msg="invalid node uuid.")
            else:
                user_error = []
                for ite in nodes:
                    if ite.phone_number in load_data['patriarch']:
                        ite.delete()
                    else:
                        new_admin = Admin(phone_number=ite, password=ite[-4:])
                        new_admin.students = [node, ]
                        try:
                            new_admin.add(new_admin)
                        except SQLAlchemyError as e:
                            user_error.append(ite)
                if user_error is False:
                    return ret_msg(status=False, msg="update some patriarches failed.", data=json.dumps(user_error))
        return ret_msg(status=True, msg="update success")
                
    @jwt_required()
    def delete(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        status, node = tm.find_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=node)
        if node.is_student:
            users = node.users
            for ite in users:
                ite.delete()
        status, error = tm.delete_node(node_uuid=node_uuid)
        if status is False:
            return ret_msg(status=False, msg=error)
        return ret_msg(status=True, msg="delete node success.")
