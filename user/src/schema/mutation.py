import typing
import strawberry
from strawberry.types import Info
from flask_jwt_extended import create_access_token

from src.models import User as UserModel
from src.schema.definitions import User as UserDefinition, Login

@strawberry.type
class UserMutation:

    @strawberry.mutation
    def user_create(self, info: Info, name: str, email: str, password: str) -> UserDefinition:

        user = UserModel(name=name, email=email, password=password)
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

    @strawberry.mutation
    def login(self, email: str, password: str) -> typing.Optional[Login]:
        try:
            user = UserModel().get_by(email=email)

            if user.verify_password(password=password):
                access_token = create_access_token(identity=user.email)
                return Login(access_token=access_token)
        except Exception as errors:
            return Login(access_token=None)


