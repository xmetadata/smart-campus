from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


class CRUD():
    def add(self, resource):
        try:
            db.session.add(resource)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False

    def update(self):
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False

    def delete(self, resource):
        try:
            db.session.delete(resource)
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
