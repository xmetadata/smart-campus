from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CRUD():
    def add(self, resource):
        db.session.add(resource)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        db.session.commit()
