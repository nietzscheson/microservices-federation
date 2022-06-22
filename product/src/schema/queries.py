from ariadne import ObjectType
from ariadne.contrib.federation import FederatedObjectType
from src.models import db, Product

query = ObjectType("Query")
product = FederatedObjectType("Product")

user = FederatedObjectType("User")

@query.field("products")
def resolve_products(_, info):
    try:
        products = [product.to_json() for product in Product.all()]

        if not products:
            raise Exception("No products")

        payload = {
            "success": True,
            "products": products
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@query.field("product")
def resolve_product(_, info, id):
    try:
        product = Product.get(id)

        if not product:
            raise Exception("The product %s doesn't exists" % id)
        payload = {
            "success": True,
            "product": product
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload


def resolve_product_reference(_, info, representation):
    try:
        product = Product.get(representation.get("id"))

        if not product:
            raise Exception("The product %s doesn't exists" % id)
        payload = product
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@product.field("createdBy")
def resolve_created_by(product, *_):
    # return {"__typename": "User", "id": product["created_by"]}
    return {"id": product["created_by"]}
