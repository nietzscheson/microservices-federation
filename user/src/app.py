import os
import typing
import strawberry
from flask import Flask
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
    JWT_SECRET_KEY = "super-secret"
    PASSWORD_TEST_USER = "1234@#example"

app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db.init_app(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

@click.command(name='fixtures')
@with_appcontext
def fixtures():

    user_admin = User(name="Admin")
    user_staff = User(name="Staff")
    user_user = User(name="User")

    db.session.add(user_admin)
    db.session.add(user_staff)
    db.session.add(user_user)

    db.session.commit()


app.cli.add_command(fixtures)

@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID
    name: str

    @classmethod
    def resolve_reference(cls, **representation) -> "UserType":

        id = strawberry.ID(representation["id"])
        user = db.session.get(User, id)

        return cls(id=user.id, name=user.name)

@strawberry.type(name="User")
class Query:
    @strawberry.field
    def user(self, info: strawberry.types.Info, id: strawberry.ID) -> UserType:

        user = db.session.get(User, id)

        if user:
            return user
        raise Exception("The user %s doesn't exists" % id)

    @strawberry.field
    def users(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[UserType]:

        return db.session.query(User).all()

@strawberry.type
class Mutation:

    @strawberry.mutation
    def user_create(self, info: strawberry.types.Info, name: str) -> UserType:

        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        return user

schema = strawberry.federation.Schema(query=Query, types=[UserType], mutation=Mutation, enable_federation_2=True)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)
