from common.database import db, CRUD

class VipType(db.Model, CRUD):
    __tablename__ = "VipType"
    id                  = db.Column(db.Integer, primary_key=True)
    vip_name            = db.Column(db.String(80), default="")
    amount              = db.Column(db.Integer, default=0)
    during              = db.Column(db.Integer, default=0)
    vip_record          = db.relationship('VipRecord', backref='VipType', lazy='dynamic')
    patriarch           = db.relationship('Patriarch', backref='VipType', lazy='dynamic')

class VipRecord(db.Model, CRUD):
    __tablename__ = "VipRecords"
    id                  = db.Column(db.Integer, primary_key=True)
    create_time         = db.Column(db.DateTime(), nullable=False)
    vip_id              = db.Column(db.Integer, db.ForeignKey('VipType.id'))
    patriarch_id        = db.Column(db.Integer, db.ForeignKey('Patriarch.id'))
