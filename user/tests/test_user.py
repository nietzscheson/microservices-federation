#def test_user_create(client):
#
#    response = client(query={
#        "query": """
#        mutation UserCreate($name: String!){
#            userCreate(name: $name){
#                errors
#                success
#                user{
#                    id
#                    name
#                }
#            }
#        }
#        """,
#        "variables": {"name": "Isabella"}}
#    )
#
#    data = response.get_json()["data"]
#    operation = data["userCreate"]
#
#    errors = operation["errors"]
#    success = operation["success"]
#    user = operation["user"]
#
#    assert errors == None
#    assert success == True
#    assert user["id"] == 1
#    assert user["name"] == "Isabella"
#
#def test_user_update(client, add_user):
#
#    user = add_user(name="Isabella")
#
#    response = client(query={
#        "query": """
#        mutation UserUpdate($id: Int!, $name: String!){
#            userUpdate(id: $id, name: $name){
#                errors
#                success
#                user{
#                    id
#                    name
#                }
#            }
#        }
#        """,
#        "variables": {"id": user.id, "name": "Emmanuel"}}
#    )
#
#    data = response.get_json()["data"]
#    operation = data["userUpdate"]
#
#    errors = operation["errors"]
#    success = operation["success"]
#    user = operation["user"]
#
#    assert errors == None
#    assert success == True
#    assert user["id"] == 1
#    assert user["name"] == "Emmanuel"
#
#def test_user_delete(client, add_user):
#
#    user = add_user(name="Isabella")
#
#    response = client(query={
#        "query": """
#        mutation UserDelete($id: Int!){
#            userDelete(id: $id){
#                errors
#                success
#            }
#        }
#        """,
#        "variables": {"id": user.id}}
#    )
#
#    data = response.get_json()["data"]
#    operation = data["userDelete"]
#
#    errors = operation["errors"]
#    success = operation["success"]
#
#    assert errors == None
#    assert success == True

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

    assert user["id"] == 1
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

