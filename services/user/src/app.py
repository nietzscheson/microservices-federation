import typing
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import Column, Integer, String

from src.database import Base
from src.containers import MainContainer

container = MainContainer()
Session = container.session()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID
    name: str

    @classmethod
    def resolve_reference(cls, **representation) -> "UserType":
        with Session() as session:
            id = strawberry.ID(representation["id"])
            user = session.get(User, id)
            return cls(id=user.id, name=user.name)


@strawberry.type(name="User")
class Query:
    @strawberry.field
    def user(self, info: strawberry.types.Info, id: strawberry.ID) -> UserType:
        with Session() as session:
            user = session.get(User, id)
            if user:
                return UserType(id=user.id, name=user.name)
            raise Exception("The user %s doesn't exists" % id)

    @strawberry.field
    def users(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[UserType]:
        with Session() as session:
            return [UserType(id=u.id, name=u.name) for u in session.query(User).all()]


@strawberry.type
class Mutation:

    @strawberry.mutation
    def user_create(self, info: strawberry.types.Info, name: str) -> UserType:
        with Session() as session:
            user = User(name=name)
            session.add(user)
            session.commit()
            return UserType(id=user.id, name=user.name)


schema = strawberry.federation.Schema(query=Query, types=[UserType], mutation=Mutation, enable_federation_2=True)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
