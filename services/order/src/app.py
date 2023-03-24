import os
import typing
import strawberry
from flask import Flask
# from src.models import db, User
from flask_migrate import Migrate
from strawberry.flask.views import GraphQLView
import click
from flask.cli import with_appcontext
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db.init_app(app)
migrate = Migrate(app, db)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    created_by = db.Column(db.Integer)
    product = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "product": self.product
        }

@click.command(name='fixtures')
@with_appcontext
def fixtures():

    order_1 = Order(name="###-001", created_by=1, product=1)
    order_2 = Order(name="###-002", created_by=2, product=2)
    order_3 = Order(name="###-003", created_by=3, product=3)

    db.session.add(order_1)
    db.session.add(order_2)
    db.session.add(order_3)

    db.session.commit()

app.cli.add_command(fixtures)

@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return UserType(id)


@strawberry.federation.type(keys=["id"])
class ProductType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return ProductType(id)

@strawberry.federation.type(keys=["id"], description="Order Type definition")
class OrderType:
    id: strawberry.ID
    name: str

    @strawberry.field
    def created_by(self) -> typing.Optional[UserType]:

        return UserType(id=self.created_by)

    @strawberry.field
    def product(self) -> typing.Optional[ProductType]:

        return ProductType(id=self.product)


@strawberry.type(name="Order")
class Query:
    @strawberry.field
    def order(self, info: strawberry.types.Info, id: strawberry.ID) -> OrderType:

        order = db.session.get(Order, id)

        if order:
            return order
        raise Exception("The Order %s doesn't exists" % id)

    @strawberry.field
    def orders(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[OrderType]:

        return db.session.query(Order).all()

@strawberry.type
class Mutation:

    @strawberry.mutation
    def order_create(self, name: str, created_by: typing.Optional[int] = None, product: typing.Optional[int] = None) -> OrderType:

        order = Order(name=name, created_by=created_by, product=product)
        db.session.add(order)
        db.session.commit()

        return order

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)
