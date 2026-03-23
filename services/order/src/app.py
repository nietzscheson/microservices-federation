import typing
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import Column, Integer, String

from src.database import Base
from src.containers import MainContainer

container = MainContainer()
Session = container.session()


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    created_by = Column(Integer)
    product = Column(Integer)


@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return UserType(id)


@strawberry.federation.type(keys=["id"])
class ProductType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return ProductType(id)


@strawberry.federation.type(keys=["id"], description="Order Type definition")
class OrderType:
    id: strawberry.ID
    name: str
    _created_by: strawberry.Private[typing.Optional[int]] = None
    _product: strawberry.Private[typing.Optional[int]] = None

    @strawberry.field
    def created_by(self) -> typing.Optional[UserType]:
        if self._created_by is not None:
            return UserType(id=self._created_by)
        return None

    @strawberry.field
    def product(self) -> typing.Optional[ProductType]:
        if self._product is not None:
            return ProductType(id=self._product)
        return None

    @classmethod
    def resolve_reference(cls, **representation) -> "OrderType":
        with Session() as session:
            id = strawberry.ID(representation["id"])
            order = session.get(Order, id)
            return cls(id=order.id, name=order.name, _created_by=order.created_by, _product=order.product)


@strawberry.type(name="Order")
class Query:
    @strawberry.field
    def order(self, info: strawberry.types.Info, id: strawberry.ID) -> OrderType:
        with Session() as session:
            order = session.get(Order, id)
            if order:
                return OrderType(id=order.id, name=order.name, _created_by=order.created_by, _product=order.product)
            raise Exception("The Order %s doesn't exists" % id)

    @strawberry.field
    def orders(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[OrderType]:
        with Session() as session:
            return [OrderType(id=o.id, name=o.name, _created_by=o.created_by, _product=o.product) for o in session.query(Order).all()]


@strawberry.type
class Mutation:

    @strawberry.mutation
    def order_create(self, name: str, created_by: typing.Optional[int] = None, product: typing.Optional[int] = None) -> OrderType:
        with Session() as session:
            order = Order(name=name, created_by=created_by, product=product)
            session.add(order)
            session.commit()
            return OrderType(id=order.id, name=order.name, _created_by=order.created_by, _product=order.product)


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
