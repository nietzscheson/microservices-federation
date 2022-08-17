from typing import Optional
import strawberry
from src.schema.query import UserQuery
from src.schema.mutation import UserMutation


@strawberry.type
class Query(UserQuery):
    _service: Optional[str]

@strawberry.type
class Mutation(UserMutation):
    _service: Optional[str]

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)

