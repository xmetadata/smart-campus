from common.database import db
from common.satree import TreeMixin
from common.schema import ma
import datetime

class NodeTree(db.Model, TreeMixin):
    __tablename__   = "NodeTree"
    title           = db.Column(db.String(50), default="")
    is_student      = db.Column(db.Boolean, default=False)
    level           = db.Column(db.Integer)
    c_time          = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#edit
##basic schema
class NodeSchema(ma.Schema):
    class Meta:
        fields = ('title','is_student', 'patriarch')

class TreeListSchema(ma.Schema):
    class Meta:
        fields = ('title', 'node_uuid', 'children')
    children = ma.Nested(NodeSchema)

##OUT->list node
class ListSchema(ma.Schema):
    class Meta:
        fields = ('title','node_uuid')

##IN->edit node
class BasicEditSchema(ma.Schema):
    class Meta:
        fields = ('action', 'node')
    node = ma.Nested(NodeSchema)