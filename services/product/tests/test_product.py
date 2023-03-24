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

    product = data["productCreate"]

    assert product["id"] == str(1)
    assert product["name"] == "T-Shirt"
    assert product["createdBy"]["id"] == str(1)


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

    product = data["product"]

    assert product["id"] == str(1)
    assert product["name"] == "Pants"
    assert product["createdBy"]["id"] == str(1)

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

    product = data["_entities"]

    assert product[0]["id"] == str(1)
    assert product[0]["name"] == "Pants"
