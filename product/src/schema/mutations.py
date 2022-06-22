from ariadne import convert_kwargs_to_snake_case, ObjectType
from src.models import db, Product


mutation = ObjectType("Mutation")

@convert_kwargs_to_snake_case
@mutation.field("productCreate")
def resolve_product_create(_, info, **kwargs):
    try:
        product = Product(
            name=kwargs["name"],
            price=kwargs["price"],
            quantity=kwargs["quantity"],
            created_by=kwargs["createdBy"]
        )
        product.save()

        payload = {
            "success": True,
            "product": product.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("productUpdate")
def resolve_product_update(_, info, **kwargs):
    try:
        product = Product.get(kwargs["id"])

        if not product:
            raise Exception("The product %s doesn't exists" % id)

        product.name = kwargs["name"]
        product.price = kwargs["price"]
        product.quantity = kwargs["quantity"]
        product.save()

        payload = {
            "success": True,
            "product": product.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("productDelete")
def resolve_product_delete(_, info, id):
    try:
        product = Product.get(id)

        if not product:
            raise Exception("The product %s doesn't exists" % id)

        product.delete()

        payload = {
            "success": True,
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload
