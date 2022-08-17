import typing
from unicodedata import name
import strawberry
from strawberry.types import Info
from src.models import User as UserModel
from src.schema.definitions import User as UserDefinition

@strawberry.type(name="User")
class UserMutation:

    @strawberry.mutation
    def user_create(self, info: Info, name: str) -> UserDefinition:

        user = UserModel(name=name)
        user.save()

        return user

    @strawberry.mutation
    def user_update(self, info: Info, id: int, name: str) -> UserDefinition:

        user = UserModel.get(id)

        if not user:
            raise Exception("The user %s doesn't exists" % id)

        user.name = name
        user.save()

        return user

    @strawberry.mutation
    def user_delete(self, info: Info, id: int) -> UserDefinition:

        user = UserModel.get(id)

        if not user:
            raise Exception("The user %s doesn't exists" % id)

        user.delete()

        return user


#    @strawberry.field
#    def users(self, info: Info) -> typing.List[UserDefinition]:
#
#        return  UserModel.all()
#
