from werkzeug.security import generate_password_hash, check_password_hash
from common.database import db, CRUD
from models.backdata import BackData
from common.schema import ma
import datetime

teachers2grades = db.Table("teachers2grades",
                           db.Column('teacher_id', db.Integer, db.ForeignKey("Teacher.id"), primary_key=True),
                           db.Column('grade_id', db.Integer, db.ForeignKey("BackData.node_id"), primary_key=True))

class Teacher(db.Model, CRUD):
    __tablename__ = "Teacher"

    id                  = db.Column(db.Integer, primary_key=True)
    username            = db.Column(db.String(80), nullable=False)
    hash_password       = db.Column(db.String(128), nullable=False)
    contact             = db.Column(db.String(20), nullable=False)
    grades              = db.relationship("BackData", secondary='teachers2grades', backref="Teacher")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.hash_password, password)

    @classmethod
    def find_by_username(cls, _username):
        return cls.query.filter(cls.username==_username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(cls.id==_id).first()

class UserSchema(ma.Schema):
    class Meta:
        fields=('username', 'password')
class UserOut(ma.Schema):
    class Meta:
        fields=('id','username')
