import typing
from unicodedata import name
import strawberry
from strawberry.types import Info
from src.models import User as UserModel
from src.schema.definitions import User as UserDefinition
from flask_jwt_extended import jwt_required

@strawberry.type(name="User")
class UserQuery:
    @jwt_required()
    @strawberry.field
    def user(self, info: Info, id: strawberry.ID) -> UserDefinition:

        user = UserModel.get(id)

        if user:
            return user
        raise Exception("The user %s doesn't exists" % id)

    @strawberry.field
    def users(self, info: Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[UserDefinition]:

        return UserModel.paginate(page=page, perPage=perPage, sortField=sortField)
