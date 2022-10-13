from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(self, id: int):
        return db.session.query(self).get(id)

    @classmethod
    def get_by(self, **kwargs):
        return db.session.query(self).filter_by(**kwargs).first()

    @classmethod
    def all(self):
        return db.session.query(self).all()

    @classmethod
    def paginate(self, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC"):

        order_by = eval(f"self.{sortField}.{sortOrder.lower()}()")

        return self.query.order_by(order_by).paginate(page,perPage, False).items

    @property
    def password(self,):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
