from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResourceModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        db.session.commit()

    @classmethod
    def get(self, id: int):
        return db.session.query(self).get(id)

    @classmethod
    def all(self):
        return db.session.query(self).all()

class Order(ResourceModel):

    created_by = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "created_by": self.created_by,
        }
