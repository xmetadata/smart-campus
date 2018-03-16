from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from common.database import db
import uuid

class TreeManager:
    def __init__(self, model_obj=None, session=None):
        self.__model   = model_obj
        self.__session = session
    def get_root_node(self):
        tmp_model = self.__model;
        return tmp_model.query.filter(tmp_model.parent_uuid=="").first()
    def add_node(self, node_uuid=None, node=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node is None:
            return False
        """add node as root"""
        if node_uuid is None:
            node.node_uuid   = uuid.uuid1()
            node.parent_uuid = ""
            node.left        = 0
            node.right       = 1
            tmp_session.add(node)
            tmp_session.commit()
            return True
        else:
            opt_node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            if opt_node is None:
                return False
            else:
                """add node as the last node of the same level"""
                node.node_uuid   = uuid.uuid1()
                node.parent_uuid = opt_node.node_uuid
                node.left        = opt_node.right
                node.right       = opt_node.right + 1
                tmp_model.query.filter(tmp_model.left>opt_node.right).update({tmp_model.left:tmp_model.left+2})
                tmp_model.query.filter(tmp_model.right>=opt_node.right).update({tmp_model.right:tmp_model.right+2})
                tmp_session.add(node)
                tmp_session.commit()
                return True
    """delete node and children"""
    def delete_node(self, node_uuid=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node_uuid is None:
            return False
        else:
            node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).one()
            if node is None:
                return False
            else:
                tmp_model.query.filter(tmp_model.left>=node.left,tmp_model.right<=node.right).delete()
                tmp_model.query.filter(tmp_model.left>node.right).update({tmp_model.left:tmp_model.left-(node.right-node.left)-1})
                tmp_model.query.filter(tmp_model.right>node.right).update({tmp_model.right:tmp_model.right-(node.right-node.left)-1})
                tmp_session.commit()
                return True
    def delete_nodes(self, node_uuids=None):
        if not isinstance(node_uuids, list):
            return False
        else:
            for id in node_uuids:
                self.delete_node(id)
            return True
    """find one node or many nodes"""
    def find_node(self, node_uuid=None, many=False, parents=False):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node_uuid is None:
            return None
        else:
            node = tmp_model.query.filter(tmp_model.node_uuid==node_uuid).first()
            if many:
                if parents:
                    return tmp_model.query.filter(tmp_model.node_uuid==node.parent_uuid).all()
                else:
                    return tmp_model.query.filter(tmp_model.parent_uuid==node.node_uuid).all()
            else:
                return node
    """update node"""
    def update_node(self, node=None):
        tmp_session = self.__session
        if node is None:
            return False
        else:
            tmp_session.commit()

class TreeMixin:
    node_uuid       = db.Column(db.String(36), primary_key=True)
    parent_uuid     = db.Column(db.String(36))
    left            = db.Column(db.Integer, default=0)
    right           = db.Column(db.Integer, default=0)
