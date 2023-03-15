from typing import Optional
import strawberry
from src.models import User as UserModel
# @strawberry.type(description="Node Response")
# class Response(object):
#     success: Optional[bool] = strawberry.field(description="Success Advice", default = True)
#     messages: Optional[list[str]] = strawberry.field(description="Success or Errors messages", default = None)

@strawberry.federation.type(keys=["id"], description="User Type definition")
class User:
    id: strawberry.ID
    name: str
    email: str

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        user = UserModel.get(id)

        if user:
            return user
        raise Exception("The user %s doesn't exists" % id)

@strawberry.type(description="Access Token")
class Login(object):
    access_token: Optional[str] = strawberry.field(description="JWT Access Token Value", default_factory = lambda: None)

    def __init__(self, *args, **kwargs) -> None:
        self.access_token = kwargs["access_token"]
