def test_user_create(client):

    response = client(query={
        "query": """
        mutation UserCreate($name: String!){
            userCreate(name: $name){
                id
                name
            }
        }
        """,
        "variables": {"name": "Isabella"}}
    )

    data = response.get_json()["data"]

    user = data["userCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "Isabella"


def test_user(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        query User($id: ID!){
            user(id: $id){
                id
                name
            }
        }
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]

    user = data["user"]

    assert user["id"] == str(1)
    assert user["name"] == "Isabella"

def test_user_representation(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
            query UserRepresentation($id: Int!){
                _entities(representations: [{ __typename: "UserType", id: $id }]) {
                ...on UserType {
                    id
                    name
                }
            }}
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]

    user = data["_entities"]

    assert user[0]["id"] == str(1)
    assert user[0]["name"] == "Isabella"
