from marshmallow import Schema, fields
from common.database import db, CRUD
from models.user import UserSchema


class ItemModel(db.Model, CRUD):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", backref=db.backref("item", lazy="dynamic"))

    def __init__(self, name, price, user_id):
        self.name = name
        self.price = price
        self.user_id = user_id


class ItemSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    user = fields.Nested(UserSchema)