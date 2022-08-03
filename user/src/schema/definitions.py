import strawberry

@strawberry.federation.type(keys=["id"], description="User Type definition")
class User:
    id: strawberry.ID
    name: str

