from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.FLOAT(precision=10, decimal_return_scale=None))
    quantity = db.Column(db.Integer)
    created_by = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "created_by": self.created_by
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: int):
        return db.session.get(cls, id)

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


