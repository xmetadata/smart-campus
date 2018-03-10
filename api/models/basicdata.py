from common.database import db
from common.satree import TreeMixin
from common.schema import ma

class BasicData(db.Model, TreeMixin):
    __tablename__   = "OrigData"
    name            = db.Column(db.String(80), nullable=False)
    sex             = db.Column(db.Integer, default=0)
    age             = db.Column(db.Integer, default=0)
    address         = db.Column(db.String(120), default='')
    identify_card   = db.Column(db.String(20), default=0)
    campus_id       = db.Column(db.String(30), default='')
    cantact         = db.Column(db.String(20), default='')

class BasicSchema(ma.Schema):
    class Meta:
        fields = ('name','sex','age','cantact','node_id')
