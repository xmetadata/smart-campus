from sqlalchemy import func
from database import db
import uuid

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
    def add_node(self, root_id=-1, node=None, level=0):
        tmp_session = self.__session
        tmp_model   = self.__model
        if node is None:
            return False
        """add node as root"""
        if root_id == -1:
            last_root = tmp_session.filter(func.max(tmp_model.root_id)).first()
            node.parent_id = 0
            node.left      = 0
            node.right     = 1
            node.level     = 0
            if last_root is None:
                node.root_id = 0
            else:
                node.root_id = last_root.root_id + 1
            tmp_session.add(node)
            tmp_session.commit()
            return True
        else:
            if level == 0:
                return False
            else:
                root       = tmp_session.query.filter(tmp_model.root_id==root_id,tmp_model.parent_id==0).one()
                node_level = tmp_session.query.filter(tmp_model.root_id==root_id,tmp_model.level==level).last()
                if node_level is None:
                    """add the node as second node of the tree"""
                    node.root_id   = root.root_id
                    node.parent_id = root.root_id
                    node.left      = root.left + 1
                    node.right     = root.left + 2
                    node.level     = level
                    tmp_session.add(node)
                    tmp_session.commit()
                    root.right = root.right + 2
                    tmp_session.update()
                    return True
                else:
                    """add the node as last one at the level"""
                    node.root_id   = node_level.root_id
                    node.parent_id = node_level.parent_id
                    node.left      = node_level.right + 1
                    node.right     = node_level.right + 2
                    node.level     = level
                    nodes = tmp_session.query.filter(tmp_model.left>next_node.right).all()
                    for iter_node in nodes:
                        iter_node.left  = iter_node.left + 2
                        iter_node.right = iter_node.right + 2
                    ref_node.right = ref_node.right + 2
                    tmp_session.update()
                    tmp_session.add(node)
                    tmp_session.commit()
                    return True
    def delete_node(self, ref_node):



class MenuList(db.Model):
    root_id         = db.Column(db.Integer, default=0)
    parent_id       = db.Column(db.Integer, default=0)
    id              = db.Column(db.Integer, default=0, primary_key=True)
    left            = db.Column(db.Integer, default=0)
    right           = db.Column(db.Integer, default=0)
    level           = db.Column(db.Integer, default=0)

    name            = db.Column(db.String(80), nullable=False)
    sex             = db.Column(db.Integer, default=0)
    age             = db.Column(db.Integer, default=0)
    address         = db.Column(db.String(120), default='')
    identify_card   = db.Column(db.String(20), default=0)
    campus_id       = db.Column(db.String(30), default='')
    cantact         = db.Column(db.String(20), default='')
