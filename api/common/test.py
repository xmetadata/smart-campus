from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from satree import TreeManager, db, TreeMixin

class MenuList(db.Model, TreeMixin):
    __tablename__   = "MenuList"
    name            = db.Column(db.String(80), nullable=False)
    sex             = db.Column(db.Integer, default=0)
    age             = db.Column(db.Integer, default=0)
    address         = db.Column(db.String(120), default='')
    identify_card   = db.Column(db.String(20), default=0)
    campus_id       = db.Column(db.String(30), default='')
    cantact         = db.Column(db.String(20), default='')

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Aa888888@192.168.11.101:16868/SmartCampus"
db.init_app(app)
app.app_context().push()
db.create_all()
tm=TreeManager(MenuList, db.session)
test1=MenuList(age=1,name="pc")
tm.add_node(node=test1)
test2=MenuList(age=2,name="pc")
tm.add_node(test1.node_uuid, test2)
test3=MenuList(age=3,name="pc")
tm.add_node(test1.node_uuid, test3)
tm.delete_node(test2.node_uuid)
node=tm.find_node(test3.node_uuid)
if node is None:
    print "None"
else:
    print node.node_uuid
node.age=666666
tm.update_node(node)
