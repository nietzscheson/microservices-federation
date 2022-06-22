from ariadne import ObjectType, convert_kwargs_to_snake_case
from src.models import User

mutation = ObjectType("Mutation")

@convert_kwargs_to_snake_case
@mutation.field("userCreate")
def resolve_user_create(_, info, name):
    try:
        user = User(name=name)
        user.save()

        payload = {
            "success": True,
            "user": user.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("userUpdate")
def resolve_user_update(_, info, id, name):
    try:
        user = User.get(id)

        if not user:
            raise Exception("The user %s doesn't exists" % id)

        user.name = name
        user.save()

        payload = {
            "success": True,
            "user": user.to_json()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload

@convert_kwargs_to_snake_case
@mutation.field("userDelete")
def resolve_user_delete(_, info, id):
    try:
        user = User.get(id)

        if not user:
            raise Exception("The user %s doesn't exists" % id)

        user.delete()

        payload = {
            "success": True,
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload
