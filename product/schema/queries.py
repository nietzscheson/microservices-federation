
from models import db, Product


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
