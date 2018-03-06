from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import uuid

db=SQLAlchemy()

class TreeManager:
    def __init__(self, model_obj=None, session=None):
        self.__model   = model_obj
        self.__session = session
    def get_root_node(self, node=None):
        tmp_model   = self.__model;
        tmp_session = self.__session;
        if node is None:
            return tmp_session.query.filter(tmp_model.parent_id==0).all()
        else:
            return tmp_session.query.filter(tmp_model.root_id==node.root_id,tmp_model.parent_id==0).first()
    def add_node(self, node_id=-1, node=None):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node is None:
            return False
        """add node as root"""
        if node_id == -1:
            node.parent_id = 0
            node.left      = 0
            node.right     = 1
            tmp_session.add(node)
            tmp_session.commit()
            return True
        else:
            opt_node = tmp_model.query.filter(tmp_model.node_id==node_id).first()
            if opt_node is None:
                return False
            else:
                """add node as the last node of the same level"""
                node.parent_id = opt_node.node_id
                node.left      = opt_node.right
                node.right     = opt_node.right + 1
                tmp_model.query.filter(tmp_model.right>=opt_node.right).update({tmp_model.right:tmp_model.right+2})
                tmp_model.query.filter(tmp_model.left>opt_node.right).update({tmp_model.right:tmp_model.right+2})
                tmp_session.add(node)
                tmp_session.commit()
                return True
    """delete node and children"""
    def delete_node(self, node_id=-1):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node_id == -1:
            return False
        else:
            node = tmp_model.query.filter(tmp_model.node_id==node_id).one()
            if node is None:
                return False
            else:
                tmp_model.query.filter(tmp_model.left>=node.left,tmp_model.right<=node.right).delete()
                tmp_model.query.filter(tmp_model.left>node.right).update({tmp_model.left:tmp_model.left-(node.right-node.left)-1})
                tmp_model.query.filter(tmp_model.right>node.right).update({tmp_model.right:tmp_model.right-(node.right-node.left)-1})
    """find one node or many nodes"""
    def find_node(self, node_id=-1, many=False):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node_id == -1:
            return None
        else:
            node = tmp_model.query.filter(tmp_model.node_id==node_id).one()
            if many:
                return tmp_model.query.filter(tmp_model.left>=node.left,tmp_model.right<=node.right).all()
            else:
                return node
    """update node"""
    def update_node(self, node=None):
        tmp_session = self.__session
        if node is None:
            return False
        else:
            tmp_session.update()

class MenuList(db.Model):
    __tablename__   = "MenuList"
    node_id         = db.Column(db.Integer, autoincrement=True, primary_key=True)
    parent_id       = db.Column(db.Integer, default=0)
    left            = db.Column(db.Integer, default=0)
    right           = db.Column(db.Integer, default=0)
    name            = db.Column(db.String(80), nullable=False)
    sex             = db.Column(db.Integer, default=0)
    age             = db.Column(db.Integer, default=0)
    address         = db.Column(db.String(120), default='')
    identify_card   = db.Column(db.String(20), default=0)
    campus_id       = db.Column(db.String(30), default='')
    cantact         = db.Column(db.String(20), default='')
