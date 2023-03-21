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

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    created_by = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by
        }

@click.command(name='fixtures')
@with_appcontext
def fixtures():

    product_1 = Product(name="T-Shirt", created_by=1)
    product_2 = Product(name="Bag", created_by=1)
    product_3 = Product(name="Pants", created_by=1)

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)

    db.session.commit()

app.cli.add_command(fixtures)

@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return UserType(id)

@strawberry.federation.type(keys=["id"], description="User Type definition")
class ProductType:
    id: strawberry.ID
    name: str

    @strawberry.field
    def created_by(self) -> typing.Optional[UserType]:

        return UserType(id=self.created_by)

    @classmethod
    def resolve_reference(cls, **representation) -> "ProductType":

        id = strawberry.ID(representation["id"])
        product = db.session.get(Product, id)

        return cls(id=product.id, name=product.name)


@strawberry.type(name="Product")
class Query:
    @strawberry.field
    def product(self, info: strawberry.types.Info, id: strawberry.ID) -> ProductType:

        product = db.session.get(Product, id)

        if product:
            return product
        raise Exception("The Product %s doesn't exists" % id)

    @strawberry.field
    def products(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[ProductType]:

        return db.session.query(Product).all()

@strawberry.type
class Mutation:

    @strawberry.mutation
    def product_create(self, name: str, created_by: typing.Optional[int] = None) -> ProductType:

        product = Product(name=name, created_by=created_by)
        db.session.add(product)
        db.session.commit()

        return product

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)
