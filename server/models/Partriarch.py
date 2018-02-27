import uuid
from sqlalchemy.sql import func
from common.database import db, CRUD

class Partriarch(db.Model, CRUD):
	part_uuid      = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
	role	       = db.Column(db.Integer,    default=0,   comment='0:expression,1:unregister,2:register')
	vip_type       = db.Column(db.Integer,    default=0,   comment='recharge vip type')
	vip_init       = db.Column(db.DateTime,   comment='vip create time')
	vip_finish     = db.Column(db.DateTime,   comment='vip expiration time')
	create_tm      = db.Column(db.DateTime,   comment='record create time', default=func.now())
	student_id     = db.Column(db.Integer,    unique=True, default=0, comment='partriarch bind student primary key')
	def __init__(self, student_id):
		self.student_id = student_id
	def set_vip(self, vip_type):
		self.vip_type   = vip_type
		self.vip_init   = func.now()
		'''self.vip_finish = ? find t_dic_viptype, get this vip valid time and set vip_finish'''