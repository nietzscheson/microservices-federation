def test_product_create(client):

    response = client(query={
        "query": """
        mutation ProductCreate($name: String!){
            productCreate(name: $name){
                id
                name
            }
        }
        """,
        "variables": {"name": "T-Shirt"}}
    )

    data = response.get_json()["data"]

    user = data["productCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "T-Shirt"


def test_product(client, add_user):

    user = add_user(name="Pants", created_by=1)

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
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]

    user = data["product"]

    assert user["id"] == str(1)
    assert user["name"] == "Pants"
    assert user["createdBy"]["id"] == str(1)
