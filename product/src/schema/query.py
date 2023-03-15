import typing
import strawberry
from strawberry.types import Info
from src.models import Product as ProductModel
from src.schema.definitions import Product as ProductDefinition

@strawberry.type(name="Product")
class ProductQuery:
    @strawberry.field
    def product(self, info: Info, id: strawberry.ID) -> ProductDefinition:

        product = ProductModel.get(id)

        if product:
            return product
        raise Exception("The Product %s doesn't exists" % id)

    @strawberry.field
    def products(self, info: Info, page: int = 1, perPage: int = 10, sortField: str = "name", sortOrder: str = "ASC") -> typing.List[ProductDefinition]:

        return ProductModel.paginate(page=page, perPage=perPage, sortField=sortField)
