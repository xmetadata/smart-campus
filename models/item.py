from common.database import db, CRUD


class ItemModel(db.Model, CRUD):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
