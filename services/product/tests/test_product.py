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

    data = response.json()["data"]

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

    data = response.json()["data"]

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

    data = response.json()["data"]

    product = data["_entities"]

    assert product[0]["id"] == str(1)
    assert product[0]["name"] == "Pants"

def test_products(client, add_product):

    add_product(name="T-Shirt", created_by=1)
    add_product(name="Pants", created_by=1)

    response = client(query={
        "query": """
        query Products{
            products{
                id
                name
                createdBy{
                    id
                }
            }
        }
        """}
    )

    data = response.json()["data"]

    products = data["products"]

    assert len(products) == 2
    assert products[0]["name"] == "T-Shirt"
    assert products[1]["name"] == "Pants"
