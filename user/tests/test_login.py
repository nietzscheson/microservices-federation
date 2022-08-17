from time import sleep
from unicodedata import name
from src.models import User

def test_login(client, add_user):

    add_user(name="Isabella", email="isabella@example.com", password="1234@#example")
    response = client(query={
        "query": """
        mutation Login($email: String!, $password: String!){
            login(email: $email, password: $password){
                accessToken
            }
        }
        """,
        "variables": {"email": "isabella@example.com", "password": "1234@#example"}}
    )

    data = response.get_json()["data"]
    login = data["login"]

#    assert user["id"] == str(1)
#    assert user["name"] == "Isabella"
