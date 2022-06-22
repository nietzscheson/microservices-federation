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
            "created_by": self.created_by,
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
    def all(self):
        return db.session.query(self).all()
