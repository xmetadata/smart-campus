from werkzeug.security import generate_password_hash, check_password_hash
from common.database import db, CRUD
from models.basicdata import BasicData
import uuid
import datetime

vip2student = db.Table('vip2student',
                    db.Column('vip_uuid', db.String(36), db.ForeignKey('Vip.uuid')),
                    db.Column('student_uuid', db.String(36), db.ForeignKey(BasicData.node_uuid)))

class Vip(db.Model):
    __tablename__   = "Vip"
    uuid            = db.Column(db.String(36), primary_key=True, default=uuid.uuid1())
    phone_number    = db.Column(db.String(11), nullable=False)
    hash_password   = db.Column(db.String(128), nullable=False)
    open_id         = db.Column(db.String(30))
    expire          = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    is_wechat       = db.Column(db.Boolean, default=False)
    is_active       = db.Column(db.Boolean, default=False)
    c_time          = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    l_time          = db.Column(db.DateTime)
    students        = db.relationship('BasicData', secondary=vip2student, lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.hash_password, password)