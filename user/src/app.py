import os
from flask import Flask, escape, request
from src.models import db
from flask_migrate import Migrate
from strawberry.flask.views import GraphQLView
from flask_jwt_extended import JWTManager

from src.command import fixtures
from src.schema import schema

app = Flask(__name__)
app.config.from_object("src.config.Config")

app.cli.add_command(fixtures)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.route('/')
def index():
    name = request.args.get("name", os.environ['NAME'])
    return f'Hello, {escape(name)}!'

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)
