import os
from flask import Flask, escape, request, jsonify
from src.models import db
from flask_migrate import Migrate
from strawberry.flask.views import GraphQLView

# from ariadne import graphql_sync, load_schema_from_path, snake_case_fallback_resolvers
# from ariadne.constants import PLAYGROUND_HTML
# from ariadne.contrib.federation import make_federated_schema

# from src.schema.queries import query, user
# from src.schema.mutations import mutation
from src.command import fixtures
from src.schema import schema
# type_defs = load_schema_from_path("src/schema/schema.graphql")

# schema = make_federated_schema(type_defs, [query, user], mutation, snake_case_fallback_resolvers)

app = Flask(__name__)
app.config.from_object("src.config.Config")

app.cli.add_command(fixtures)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    name = request.args.get("name", os.environ['NAME'])
    return f'Hello, {escape(name)}!'

# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     return PLAYGROUND_HTML, 200


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#     data = request.get_json()
#     success, result = graphql_sync(
#         schema,
#         data,
#         context_value=request,
#         debug=app.debug
#     )
#
#     status_code = 200 if success else 400
#     return jsonify(result), status_code
