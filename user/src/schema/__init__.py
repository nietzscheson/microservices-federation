from typing import Optional
import strawberry
from strawberry.schema.config import StrawberryConfig
from src.schema.query import User
from src.schema.definitions import User as UserDefinition


@strawberry.type
class Query(User):
    pass

schema = strawberry.federation.Schema(Query, config=StrawberryConfig(auto_camel_case=False))

