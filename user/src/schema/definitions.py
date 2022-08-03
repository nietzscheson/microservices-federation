import strawberry

@strawberry.federation.type(extend=True, keys=["id"], description="User Type definition")
class User:
    id: int = strawberry.federation.field(external=True)
    name: str

    @classmethod
    def resolve_reference(cls, id: int):
        # here we could fetch the book from the database
        # or even from an API
        return User(id=id)
