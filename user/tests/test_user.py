def test_user_create(client):

    response = client(query={
        "query": """
        mutation UserCreate($name: String!){
            userCreate(name: $name){
                errors
                success
                user{
                    id
                    name
                }
            }
        }
        """,
        "variables": {"name": "Isabella"}}
    )

    data = response.get_json()["data"]
    user_create = data["userCreate"]

    errors = user_create["errors"]
    success = user_create["success"]
    user = user_create["user"]

    assert errors == None
    assert success == True
    assert user["id"] == 1
    assert user["name"] == "Isabella"

def test_user_update(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        mutation UserUpdate($id: Int!, $name: String!){
            userUpdate(id: $id, name: $name){
                errors
                success
                user{
                    id
                    name
                }
            }
        }
        """,
        "variables": {"id": user.id, "name": "Emmanuel"}}
    )

    data = response.get_json()["data"]
    user_update = data["userUpdate"]

    errors = user_update["errors"]
    success = user_update["success"]
    user = user_update["user"]

    assert errors == None
    assert success == True
    assert user["id"] == 1
    assert user["name"] == "Emmanuel"

def test_user_delete(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        mutation UserDelete($id: Int!){
            userDelete(id: $id){
                errors
                success
            }
        }
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]
    user_delete = data["userDelete"]

    errors = user_delete["errors"]
    success = user_delete["success"]

    assert errors == None
    assert success == True

def test_user(client, add_user):

    user = add_user(name="Isabella")

    response = client(query={
        "query": """
        query User($id: Int!){
            user(id: $id){
                errors
                success
                user{
                    id
                    name
                }
            }
        }
        """,
        "variables": {"id": user.id}}
    )

    data = response.get_json()["data"]
    user = data["user"]

    errors = user["errors"]
    success = user["success"]
    user = user["user"]

    assert errors == None
    assert success == True
    assert user["id"] == 1
    assert user["name"] == "Isabella"

def test_users(client, add_user):

    add_user(name="Isabella")
    add_user(name="Emmanuel")

    response = client(query={
        "query": """
        query Users{
            users{
                errors
                success
                users{
                    id
                    name
                }
            }
        }
        """,
        "variables": {}}
    )

    data = response.get_json()["data"]
    users = data["users"]

    errors = users["errors"]
    success = users["success"]
    users = users["users"]

    assert errors == None
    assert success == True
    assert len(users) == 2
