from src.config import Config

def test_login(client, add_user):

    password = Config.PASSWORD_TEST_USER
    user = add_user(name="Isabella", email="isabella@example.com", password=password)
    response = client(query={
        "query": """
        mutation Login($email: String!, $password: String!){
            login(email: $email, password: $password){
                accessToken

            }
        }
        """,
        "variables": {"email": user.email, "password": password}}
    )

    data = response.get_json()["data"]

    login = data["login"]

    assert login["accessToken"] is not None
