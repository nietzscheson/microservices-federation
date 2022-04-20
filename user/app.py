import imp
import os
from flask import Flask, escape, request, jsonify
from models import db, User
from flask_migrate import Migrate

from ariadne import QueryType, graphql_sync, make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from schema.queries import resolve_users, resolve_user
from schema.mutations import resolve_user_create, resolve_user_update, resolve_user_delete

query = ObjectType("Query")
query.set_field("users", resolve_users)
query.set_field("user", resolve_user)

mutation = ObjectType("Mutation")
mutation.set_field("userCreate", resolve_user_create)
mutation.set_field("userUpdate", resolve_user_update)
mutation.set_field("userDelete", resolve_user_delete)

type_defs = load_schema_from_path("schema/schema.graphql")

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    name = request.args.get("name", os.environ['NAME'])
    return f'Hello, {escape(name)}!'

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
