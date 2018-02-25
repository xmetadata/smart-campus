from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


class CRUD():
    def add(self, resource):
        try:
            db.session.add(resource)
            db.session.commit()
            return True, 'resource created successfully.'
        except SQLAlchemyError as e:
            return False, e.message

    def update(self):
        try:
            db.session.commit()
            return True, 'resource updated successfully.'
        except SQLAlchemyError as e:
            return False, e.message

    def delete(self, resource):
        try:
            db.session.delete(resource)
            return True, 'resource deleted successfully.'
        except SQLAlchemyError as e:
            return False, e.message
