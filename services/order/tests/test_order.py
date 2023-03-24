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

    order = data["orderCreate"]

    assert order["id"] == str(1)
    assert order["name"] == "###-0001"


def test_order(client, add_order):

    order = add_order(name="###-0001", created_by=1, product=1)

    response = client(query={
        "query": """
        query Order($id: ID!){
            order(id: $id){
                id
                name
                createdBy{
                    id
                }
                product{
                    id
                }
            }
        }
        """,
        "variables": {"id": order.id}}
    )

    data = response.get_json()["data"]

    order = data["order"]

    assert order["id"] == str(1)
    assert order["name"] == "###-0001"
    assert order["createdBy"]["id"] == str(1)
    assert order["product"]["id"] == str(1)
