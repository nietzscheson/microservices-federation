from ariadne import convert_kwargs_to_snake_case, ObjectType
from src.models import Order


mutation = ObjectType("Mutation")

@convert_kwargs_to_snake_case
@mutation.field("orderCreate")
def resolve_order_create(_, info, **kwargs):
    try:
        order = Order(
            created_by=kwargs["createdBy"]
        )
        order.save()

        payload = {
            "success": True,
            "order": order.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("orderUpdate")
def resolve_order_update(_, info, **kwargs):
    try:
        id = kwargs["id"]
        order = Order.get(id)

        if not order:
            raise Exception("The order %s doesn't exists" % id)

        order.update(**kwargs)

        payload = {
            "success": True,
            "order": order.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("orderDelete")
def resolve_order_delete(_, info, id):
    try:
        order = Order.get(id)

        if not order:
            raise Exception("The order %s doesn't exists" % id)

        order.delete()

        payload = {
            "success": True,
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload
