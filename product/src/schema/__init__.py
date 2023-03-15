from typing import Optional
import strawberry
from src.schema.query import ProductQuery
from src.schema.mutation import ProductMutation


@strawberry.type
class Query(ProductQuery):
    _service: Optional[str]

@strawberry.type
class Mutation(ProductMutation):
    _service: Optional[str]

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

