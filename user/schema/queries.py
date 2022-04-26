
from models import db, User

def resolve_hello(_, info):
    return "Hello!"


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
