import email
from typing import Optional
import strawberry

@strawberry.federation.type(keys=["id"], description="User Type definition")
class User:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type(description="Access Token")
class Login(object):
    access_token: Optional[str] = strawberry.field(description="JWT Access Token Value")
