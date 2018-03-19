from flask_restful import Resource, request
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from common.satree import TreeManager
from common.database import db
from common.retmsg import ret_msg
from models.nodetree import NodeTree, ListSchema, BasicEditSchema, NodeSchema, TreeListSchema
from models.admin import Admin
import datetime
import json

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
            load_data, errors = NodeSchema(exclude=('patriarch')).loads(req_json)
            if errors:
                return ret_msg(status=False, msg="parse request data failed.")
            root = NodeTree(title=load_data['title'], is_student=load_data['is_student'])
            try:
                tm.add_node(node=root)
            except SQLAlchemyError as e:
                return ret_msg(status=False, msg=e.message)
            return ret_msg(status=False, msg="add root node success.")

class TreeList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed."), 400
        basic_node = tm.find_node(node_uuid=node_uuid)
        if basic_node is None:
            return ret_msg(status=False, msg="invalid node uuid"), 404
        nodes = tm.find_node(node_uuid=basic_node.node_uuid, many=True)
        ret_data = {"title" : basic_node.title, "node_uuid" : basic_node.node_uuid, "children" : ""}
        ret_data.children = NodeSchema(many=True, exclude=('patriarch')).dump(nodes).data
        return ret_msg(status=True, msg="find success", data=ret_data), 200

class TreeEdit(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        node = tm.find_node(node_uuid=node_uuid)
        if node is None:
            return ret_msg(status=False, msg="invalid node uuid.")
        return ret_msg(status=True, msg="find node success", data=NodeSchema(exclude=('patriarch')).dump(node).data)
    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed.")
        basic_node = tm.find_node(node_uuid=node_uuid)
        if basic_node is None:
            return ret_msg(status=False, msg="invalid node uuid.")
        req_json = json.dumps(request.get_json())
        load_data, errors = NodeSchema().loads(req_json)
        if errors:
            return ret_msg(status=False, msg="parse request data failed.")
        if load_data['is_student']:
            new_node = NodeTree(title=load_data['title'], is_student=load_data['is_student'])
            try:
                ret = tm.add_node(new_node)


        new_node = NodeTree(title=load_data['title'], is_student=load_data['is_student'])
    @jwt_required()
    def put(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed."), 400
    @jwt_required()
    def delete(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if tm is None:
            return ret_msg(status=False, msg="get manager handle failed."), 400

class NodeDetail(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)

class BasicList(Resource):
    @jwt_required()
    def get(self, node_uuid):
        tm=TreeManager(NodeTree, db.session)
        basic_node = None
        if node_uuid == "root":
            root = tm.get_root_node()
            if root is None:
                root = NodeTree(title="smart school", is_student=False, c_time=datetime.datetime.utcnow())
                tm.add_node(node=root)
                return {"title" : root.title, "node_uuid" : root.node_uuid, "children" : []}, 200
            basic_node = root
        else:
            basic_node = tm.find_node(node_uuid=node_uuid)
        nodes = tm.find_node(node_uuid=basic_node.node_uuid, many=True)
        return {"title" : basic_node.title, "node_uuid" : basic_node.node_uuid, "children" : ListSchema(many=True).dump(nodes).data}, 200

class BasicEdit(Resource):
    @jwt_required()
    def post(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        req_data = json.dumps(request.get_json())
        load_data, errors = BasicEditSchema().loads(req_data)
        if errors:
            return errors, 400
        basic_node = tm.find_node(node_uuid=node_uuid)
        if basic_node is None:
            return {"msg" : "invalid node_uuid"}, 400
        if load_data['action'] == 'add':
            if load_data['node']['is_student']:
                student_node = NodeTree(title=load_data['node']['title'], is_student=load_data['node']['is_student'])
                ret = tm.add_node(node_uuid=basic_node.node_uuid, node=student_node)
                if ret is False:
                    return {"msg" : "add failed"}, 400
                patriarch_list = load_data['node']['patriarch']
                patriarch_error = []
                for patriarch_itr in patriarch_list:
                    tmp_admin = Admin(phone_number=patriarch_itr, password=patriarch_itr[-4:])
                    tmp_admin.students = [student_node,]
                    try:
                        tmp_admin.add(tmp_admin)
                    except SQLAlchemyError as e:
                        patriarch_error.append(patriarch_itr)
                if patriarch_error is False:
                    return {"msg" : "add failed", "patriarch" : json.dumps(patriarch_error)},200
                else:
                    return {"msg" : "add success", "patriarch" : []}, 400
            else:
                node = NodeTree(title=load_data['node']['title'], is_student=load_data['node']['is_student'])
                try:
                    tm.add_node(node_uuid=basic_node.node_uuid, node=node)
                except SQLAlchemyError as e:
                    return {'msg': e.message}, 400
            return {"msg" : "add success"}, 200
        elif load_data['action'] ==  'update':
            basic_node.title = load_data['node']['title']
            tm.update_node(basic_node)
            return {"msg" : "update success"}, 200
        else:
            return {"msg" : "invalid action"}, 400

    @jwt_required()
    def delete(self, node_uuid):
        tm = TreeManager(NodeTree, db.session)
        if node_uuid == 'delete':
            """delete multiple nodes"""
            req_data   = json.dumps(request.get_json())
            load_data  = json.loads(req_data)
            error_node = []
            for node_ite in load_data:
                try:
                    ret = tm.delete_node(node_ite)
                    if ret is False:
                        error_node.append(node_ite)
                except SQLAlchemyError as e:
                    error_node.append(node_ite)
            if error_node is False:
                return {"msg" : "delete failed", "nodes" : json.dumps(error_node)}, 400
            else:
                return {"msg" : "delete success", "nodes" : []}, 200
        else:
            """delete one node"""
            try:
                basic_node = tm.find_node(node_uuid=node_uuid)
            except SQLAlchemyError as e:
                return {"msg" : e.message}, 400
            if basic_node is None:
                return {"msg" : "invalid node_uuid"}, 400
            ret = tm.delete_node(node_uuid)
            return {"msg" : "delete success" if ret else "delete failed"}, 200
