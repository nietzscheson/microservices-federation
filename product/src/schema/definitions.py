import strawberry

@strawberry.federation.type(keys=["id"], description="User Type definition")
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)

@strawberry.federation.type(keys=["id"], description="Product Type definition")
class Product:
    id: strawberry.ID
    name: str
    price: float
    quantity: int
    created_by: User


    class Meta:
        # Specify the id field as the key for the Product type
        # and extend the User type
        # interfaces = (strawberry.interface.Node,)
        extends = ('User',)
