def test_order_create(client):

    response = client(query={
        "query": """
        mutation OrderCreate($name: String!){
            orderCreate(name: $name){
                id
                name
            }
        }
        """,
        "variables": {"name": "###-0001"}}
    )

    data = response.get_json()["data"]

    user = data["orderCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "###-0001"


def test_order(client, add_order):

    user = add_order(name="###-0001", created_by=1, product_id=1)

    response = client(query={
        "query": """
        query Order($id: ID!){
            order(id: $id){
                id
                name
                createdBy{
                    id
                }
                productId{
                    id
                }
            }
        }
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]

    user = data["order"]

    assert user["id"] == str(1)
    assert user["name"] == "###-0001"
    assert user["createdBy"]["id"] == str(1)
    assert user["productId"]["id"] == str(1)
