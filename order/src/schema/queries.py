from ariadne import ObjectType
from ariadne.contrib.federation import FederatedObjectType
from src.models import Order

query = ObjectType("Query")
order = FederatedObjectType("Order")

user = FederatedObjectType("User")

@query.field("orders")
def resolve_orders(_, info):
    try:
        orders = [order.to_json() for order in Order.all()]

        if not orders:
            raise Exception("No orders")

        payload = {
            "success": True,
            "orders": orders
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@query.field("order")
def resolve_order(_, info, id):
    try:
        order = Order.get(id)

        if not order:
            raise Exception("The order %s doesn't exists" % id)
        payload = {
            "success": True,
            "product": order
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload


def resolve_order_reference(_, info, representation):
    try:
        order = Order.get(representation.get("id"))

        if not order:
            raise Exception("The order %s doesn't exists" % id)
        payload = order
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@order.field("createdBy")
def resolve_created_by(order, *_):
    # return {"__typename": "User", "id": product["created_by"]}
    return {"id": order["createdBy"]}
