from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from common.database import db, CRUD
from common.schema import ma
from common.retmsg import ret_msg
from models.nodetree import NodeTree
import uuid
import datetime

admin_m2m_node = db.Table('admin_m2m_node',
                    db.Column('vip_uuid', db.String(36), db.ForeignKey('Admin.uuid')),
                    db.Column('node_uuid', db.String(36), db.ForeignKey('NodeTree.node_uuid')))

class Admin(db.Model, CRUD):
    __tablename__   = "Admin"
    uuid            = db.Column(db.String(36), primary_key=True)
    phone_number    = db.Column(db.String(11), nullable=False)
    hash_password   = db.Column(db.String(128), nullable=False)
    open_id         = db.Column(db.String(30))
    expire          = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    role            = db.Column(db.Integer, default=False)
    is_active       = db.Column(db.Boolean, default=False)
    c_time          = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    l_time          = db.Column(db.DateTime)
    nodes           = db.relationship('NodeTree', secondary=admin_m2m_node, lazy="dynamic", backref=db.backref('users', lazy='joined'))

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.hash_password, password)

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.query.filter(cls.phone_number==phone_number).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter(cls.uuid==uuid).first()

class LoginSchema(ma.Schema):
    class Meta:
        fields = ('phone_number','password','user_type')
class AdminTestSchema(ma.Schema):
    class Meta:
        fields = ('phone_number', 'hash_password', 'role')
