def test_product_create(client):

    response = client(query={
        "query": """
        mutation ProductCreate($name: String!, $createdBy: Int!){
            productCreate(name: $name, createdBy: $createdBy){
                id
                name
                createdBy {
                    id
                }
            }
        }
        """,
        "variables": {"name": "T-Shirt", "createdBy": 1}}
    )

    data = response.get_json()["data"]

    user = data["productCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "T-Shirt"
    assert user["createdBy"]["id"] == str(1)


def test_product(client, add_product):

    product = add_product(name="Pants", created_by=1)

    response = client(query={
        "query": """
        query Product($id: ID!){
            product(id: $id){
                id
                name
                createdBy{
                    id
                }
            }
        }
        """,
        "variables": {"id": product.id}}
    )

    data = response.get_json()["data"]

    user = data["product"]

    assert user["id"] == str(1)
    assert user["name"] == "Pants"
    assert user["createdBy"]["id"] == str(1)

def test_product_representation(client, add_product):

    product = add_product(name="Pants")

    response = client(query={
        "query": """
            query UserRepresentation($id: Int!){
                _entities(representations: [{ __typename: "ProductType", id: $id }]) {
                ...on ProductType {
                    id
                    name
                }
            }}
        """,
        "variables": {"id": product.id}}
    )

    data = response.get_json()["data"]

    user = data["_entities"]

    assert user[0]["id"] == str(1)
    assert user[0]["name"] == "Pants"
