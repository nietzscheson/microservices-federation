import typing
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import Column, Integer, String

from src.database import Base
from src.containers import MainContainer

container = MainContainer()
Session = container.session()


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    created_by = Column(Integer)


@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID = strawberry.federation.field

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return UserType(id)


@strawberry.federation.type(keys=["id"], description="Product Type definition")
class ProductType:
    id: strawberry.ID
    name: str
    _created_by: strawberry.Private[typing.Optional[int]] = None

    @strawberry.field
    def created_by(self) -> typing.Optional[UserType]:
        if self._created_by is not None:
            return UserType(id=self._created_by)
        return None

    @classmethod
    def resolve_reference(cls, **representation) -> "ProductType":
        with Session() as session:
            id = strawberry.ID(representation["id"])
            product = session.get(Product, id)
            return cls(id=product.id, name=product.name, _created_by=product.created_by)


@strawberry.type(name="Product")
class Query:
    @strawberry.field
    def product(self, info: strawberry.types.Info, id: strawberry.ID) -> ProductType:
        with Session() as session:
            product = session.get(Product, id)
            if product:
                return ProductType(id=product.id, name=product.name, _created_by=product.created_by)
            raise Exception("The Product %s doesn't exists" % id)

    @strawberry.field
    def products(self, info: strawberry.types.Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[ProductType]:
        with Session() as session:
            return [ProductType(id=p.id, name=p.name, _created_by=p.created_by) for p in session.query(Product).all()]


@strawberry.type
class Mutation:

    @strawberry.mutation
    def product_create(self, name: str, created_by: typing.Optional[int] = None) -> ProductType:
        with Session() as session:
            product = Product(name=name, created_by=created_by)
            session.add(product)
            session.commit()
            return ProductType(id=product.id, name=product.name, _created_by=product.created_by)


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
