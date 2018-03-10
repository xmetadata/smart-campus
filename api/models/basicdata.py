from common.database import db
from common.satree import TreeMixin
from common.schema import ma
import datetime

class BasicData(db.Model, TreeMixin):
    __tablename__   = "BasicData"
    title           = db.Column(db.String(50), default="")
    is_student      = db.Column(db.Boolean, default=False)
    level           = db.Column(db.Integer)
    c_time          = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class BasicSchema(ma.Schema):
    class Meta:
        fields = ('title','is_student')
