from time import sleep
from src.models import User

def test_user_create(client):

    response = client(query={
        "query": """
        mutation UserCreate($name: String!, $email: String!, $password: String!){
            userCreate(name: $name, email: $email, password: $password){
                id
                name
                email
            }
        }
        """,
        "variables": {"name": "Isabella", "email": "isabella@example.com", "password": "1234@#example"}}
    )

    data = response.get_json()["data"]
    user = data["userCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "Isabella"

def test_user_update(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        mutation UserUpdate($id: Int!, $name: String!){
            userUpdate(id: $id, name: $name){
                id
                name
            }
        }
        """,
        "variables": {"id": user.id, "name": "Emmanuel"}}
    )

    data = response.get_json()["data"]
    user = data["userUpdate"]

    assert user["id"] == str(1)
    assert user["name"] == "Emmanuel"

def test_user_delete(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        mutation UserDelete($id: Int!){
            userDelete(id: $id){
                id
                name
            }
        }
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]
    user = data["userDelete"]

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

def test_users(client, add_user):

    add_user(name="Isabella")
    add_user(name="Emmanuel")

    response = client(query={
        "query": """
        query Users{
            users{
                id
                name
            }
        }
        """,
        "variables": {}}
    )

    data = response.get_json()["data"]

    users = data["users"]
    assert len(users) == 2

