from time import sleep
from src.models import Product

def test_product_create(client):

    response = client(query={
        "query": """
        mutation ProductCreate($name: String!, $price: Float!, $quantity: Int!){
            productCreate(name: $name, price: $price, quantity: $quantity){
                id
                name
                price
                quantity
                createdBy
            }
        }
        """,
        "variables": {"name": "T-Shirt", "price": 10.5, "quantity": 3}}
    )

    data = response.get_json()["data"]
    user = data["productCreate"]

    assert user["id"] == str(1)
    assert user["name"] == "T-Shirt"

def test_product_update(client, add_product):

    user = add_product(name="T-Shirt", created_by=1)

    response = client(query={
        "query": """
        mutation ProductUpdate($id: Int!, $name: String!){
            productUpdate(id: $id, name: $name){
                id
                name
                createdBy
            }
        }
        """,
        "variables": {"id": user.id, "name": "T-Shirt"}}
    )

    data = response.get_json()["data"]
    product = data["productUpdate"]

    assert product["id"] == str(1)
    assert product["name"] == "T-Shirt"
    assert product["createdBy"] == 1

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

