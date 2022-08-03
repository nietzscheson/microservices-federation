from typing import Optional
import strawberry
from strawberry.schema.config import StrawberryConfig
from src.schema.query import User


@strawberry.type
class Query(User):
    _service: Optional[str]

schema = strawberry.federation.Schema(Query)

