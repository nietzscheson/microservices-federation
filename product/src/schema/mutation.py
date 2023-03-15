import typing
import strawberry
from strawberry.types import Info

from src.models import Product as ProductModel
from src.schema.definitions import Product as ProductDefinition

@strawberry.type
class ProductMutation:

    @strawberry.mutation
    def product_create(self, info: Info, name: str, price: float, quantity: int) -> ProductDefinition:

        product = ProductModel(name=name, price=price, quantity=quantity, created_by=1)
        product.save()

        return product

    @strawberry.mutation
    def product_update(self, info: Info, id: int, name: str) -> ProductDefinition:

        product = ProductModel.get(id)

        if not product:
            raise Exception("The Product %s doesn't exists" % id)

        product.name = name
        product.save()

        return product

    @strawberry.mutation
    def product_delete(self, info: Info, id: int) -> ProductDefinition:

        product = ProductModel.get(id)

        if not product:
            raise Exception("The Product %s doesn't exists" % id)

        product.delete()

        return product


