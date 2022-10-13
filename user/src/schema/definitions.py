import email
from typing import Optional
import strawberry

# @strawberry.type(description="Node Response")
# class Response(object):
#     success: Optional[bool] = strawberry.field(description="Success Advice", default = True)
#     messages: Optional[list[str]] = strawberry.field(description="Success or Errors messages", default = None)

@strawberry.federation.type(keys=["id"], description="User Type definition")
class User:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type(description="Access Token")
class Login(object):
    access_token: Optional[str] = strawberry.field(description="JWT Access Token Value", default_factory = lambda: None)

    def __init__(self, *args, **kwargs) -> None:
        self.access_token = kwargs["access_token"]
