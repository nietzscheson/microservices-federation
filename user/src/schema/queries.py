from ariadne import ObjectType
from ariadne.contrib.federation import FederatedObjectType
from src.models import User

query = ObjectType("Query")
user = FederatedObjectType("User")

@query.field("users")
def resolve_users(_, info):
    try:
        users = [user.to_json() for user in User.all()]

        if not users:
            raise Exception("No users")

        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@query.field("user")
def resolve_user(_, info, id):
    try:
        user = User.get(id)

        if not user:
            raise Exception("The user %s doesn't exists" % id)
        payload = {
            "success": True,
            "user": user
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@user.reference_resolver
def resolve_user_reference(_, info, representation):
    try:
        user = User.get(representation.get("id"))

        if not user:
            raise Exception("The user %s doesn't exists" % id)
        payload = user
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload
