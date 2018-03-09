from werkzeug.security import generate_password_hash, check_password_hash
from common.database import db, CRUD
from models.backdata import BackData
from common.schema import ma

patriarch2grades = db.Table("teachers2grades",
                           db.Column('patriarch_id', db.Integer, db.ForeignKey("Patriarch.id"), primary_key=True),
                           db.Column('student_id', db.Integer, db.ForeignKey("BackData.node_id"), primary_key=True))

class Patriarch(db.Model):
    __tablename__ = "Patriarch"
    id                  = db.Column(db.Integer, primary_key=True)
    username            = db.Column(db.String(80), nullable=False)
    hash_password       = db.Column(db.String(128), nullable=False)
    address             = db.Column(db.String(256), default='')
    contact             = db.Column(db.String(20), nullable=False)
    vip_payment         = db.Column(db.Integer, default=0)


    students            = db.relationship("BackData", secondary='patriarch2grades', backref="Teacher")
