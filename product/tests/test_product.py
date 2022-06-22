def test_product_create(client):

    response = client(query={
        "query": """
        mutation ProductCreate($name: String!, $price: Float!, $quantity: Int!, $createdBy: Int!){
            productCreate(name: $name, price: $price, quantity: $quantity, createdBy: $createdBy){
                errors
                success
                product{
                    id
                    name
                }
            }
        }
        """,
        "variables": {"name": "T-Shirt", "price": 10.5, "quantity": 3, "createdBy":1}}
    )

    data = response.get_json()["data"]
    operation = data["productCreate"]

    errors = operation["errors"]
    success = operation["success"]
    product = operation["product"]

    assert errors == None
    assert success == True
    assert product["id"] == 1
    assert product["name"] == "T-Shirt"

def test_product_update(client, add_product):

    product = add_product()

    response = client(query={
        "query": """
        mutation ProductUpdate($id: Int!, $name: String!, $quantity: Int!, $price: Float!){
            productUpdate(id: $id, name: $name, quantity: $quantity, price: $price){
                errors
                success
                product{
                    id
                    name
                    quantity
                    price
                }
            }
        }
        """,
        "variables": {"id": product.id, "name": "Pants", "quantity": 20, "price": 100.0}}
    )

    data = response.get_json()["data"]
    operation = data["productUpdate"]

    errors = operation["errors"]
    success = operation["success"]
    product = operation["product"]

    assert errors == None
    assert success == True
    assert product["id"] == 1
    assert product["name"] == "Pants"
    assert product["quantity"] == 20
    assert product["price"] == 100.0

def test_product_delete(client, add_product):
    product = add_product()

    response = client(query={
        "query": """
        mutation ProductDelete($id: Int!){
            productDelete(id: $id){
                errors
                success
            }
        }
        """,
        "variables": {"id": product.id}}
    )
    data = response.get_json()["data"]
    operation = data["productDelete"]
    errors = operation["errors"]
    success = operation["success"]
    assert errors == None
    assert success == True

def test_product(client, add_product):
    product = add_product()

    response = client(query={
        "query": """
        query Product($id: Int!){
            product(id: $id){
                errors
                success
                product{
                    id
                    name
                }
            }
        }
        """,
        "variables": {"id": product.id}}
    )
    data = response.get_json()["data"]
    operation = data["product"]
    errors = operation["errors"]
    success = operation["success"]
    product = operation["product"]
    assert errors == None
    assert success == True
    assert product["id"] == 1
    assert product["name"] == "T-Shirt"

def test_products(client, add_product):

    add_product(name="Monitor")
    add_product(name="Keyboard")

    response = client(query={
        "query": """
        query Products{
            products{
                errors
                success
                products{
                    id
                    name
                }
            }
        }
        """,
        "variables": {}}
    )

    data = response.get_json()["data"]
    operation = data["products"]

    errors = operation["errors"]
    success = operation["success"]
    products = operation["products"]

    assert errors == None
    assert success == True
    assert len(products) == 2
