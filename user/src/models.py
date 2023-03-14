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
        return db.session.get(self, id)

    @classmethod
    def get_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def paginate(cls, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC"):

        order_by = eval(f"cls.{sortField}.{sortOrder.lower()}()")

        return db.paginate(db.select(cls).order_by(order_by), page=page, max_per_page=perPage).items

    @property
    def password(self,):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
