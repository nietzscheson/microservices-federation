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

    data = response.json()["data"]

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

    data = response.json()["data"]

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

    data = response.json()["data"]

    user = data["_entities"]

    assert user[0]["id"] == str(1)
    assert user[0]["name"] == "Isabella"

def test_users(client, add_user):

    add_user(name="Isabella")
    add_user(name="Fernando")

    response = client(query={
        "query": """
        query Users{
            users{
                id
                name
            }
        }
        """}
    )

    data = response.json()["data"]

    users = data["users"]

    assert len(users) == 2
    assert users[0]["name"] == "Isabella"
    assert users[1]["name"] == "Fernando"
