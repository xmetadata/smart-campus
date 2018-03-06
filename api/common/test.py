from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from satree import TreeManager, MenuList, db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Aa888888@192.168.74.128:16868/SmartCampus"
db.init_app(app)
app.app_context().push()
db.create_all()
tm=TreeManager(MenuList, db.session)
test1=MenuList(age=1,name="pc")
tm.add_node(node=test1)
test2=MenuList(age=2,name="pc")
tm.add_node(test1.node_id, test2)
test3=MenuList(age=3,name="pc")
tm.add_node(test1.node_id, test3)
