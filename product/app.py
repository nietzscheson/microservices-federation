import os
from flask import Flask, escape, request, jsonify
from models import db
from flask_migrate import Migrate

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema
from schema.queries import resolve_products, resolve_product, resolve_product_reference
from schema.mutations import resolve_product_create, resolve_product_update, resolve_product_delete

query = ObjectType("Query")
query.set_field("products", resolve_products)
query.set_field("product", resolve_product)
product = FederatedObjectType("Product")
product.reference_resolver(resolve_product_reference)

user = FederatedObjectType("User")

mutation = ObjectType("Mutation")
mutation.set_field("productCreate", resolve_product_create)
mutation.set_field("productUpdate", resolve_product_update)
mutation.set_field("productDelete", resolve_product_delete)

type_defs = load_schema_from_path("schema/schema.graphql")

schema = make_federated_schema(type_defs, [query, product, user], mutation, snake_case_fallback_resolvers)

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
