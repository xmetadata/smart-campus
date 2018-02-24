from common.database import db, CRUD
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model, CRUD):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    hash_password = db.Column(db.String(128))

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
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
