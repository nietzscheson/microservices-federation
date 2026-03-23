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

    data = response.json()["data"]

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

    data = response.json()["data"]

    order = data["order"]

    assert order["id"] == str(1)
    assert order["name"] == "###-0001"
    assert order["createdBy"]["id"] == str(1)
    assert order["product"]["id"] == str(1)


def test_order_create_with_relationships(client):

    response = client(query={
        "query": """
        mutation OrderCreate($name: String!, $createdBy: Int!, $product: Int!){
            orderCreate(name: $name, createdBy: $createdBy, product: $product){
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
        "variables": {"name": "###-0002", "createdBy": 1, "product": 1}}
    )

    data = response.json()["data"]

    order = data["orderCreate"]

    assert order["id"] == str(1)
    assert order["name"] == "###-0002"
    assert order["createdBy"]["id"] == str(1)
    assert order["product"]["id"] == str(1)


def test_orders(client, add_order):

    add_order(name="###-0001", created_by=1, product=1)
    add_order(name="###-0002", created_by=2, product=2)

    response = client(query={
        "query": """
        query Orders{
            orders{
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
        """}
    )

    data = response.json()["data"]

    orders = data["orders"]

    assert len(orders) == 2
    assert orders[0]["name"] == "###-0001"
    assert orders[1]["name"] == "###-0002"


def test_order_representation(client, add_order):

    order = add_order(name="###-0001", created_by=1, product=1)

    response = client(query={
        "query": """
            query OrderRepresentation($id: Int!){
                _entities(representations: [{ __typename: "OrderType", id: $id }]) {
                ...on OrderType {
                    id
                    name
                }
            }}
        """,
        "variables": {"id": order.id}}
    )

    data = response.json()["data"]

    order = data["_entities"]

    assert order[0]["id"] == str(1)
    assert order[0]["name"] == "###-0001"
