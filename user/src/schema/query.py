import typing
import strawberry
from strawberry.types import Info
from src.models import User as UserModel
from src.schema.definitions import User as UserDefinition

@strawberry.type
class User:

    @strawberry.field
    def user(self, info: Info, id: strawberry.ID) -> UserDefinition:

        user = UserModel.get(id)

        if user:
            return user
        raise Exception("The user %s doesn't exists" % id)

    @strawberry.field
    def users(self, info: Info) -> typing.List[UserDefinition]:

        return  UserModel.all()
