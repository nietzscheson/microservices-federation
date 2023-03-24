import pytest
from src.app import app as _app, db as _db, Product
from sqlalchemy import event


@pytest.fixture(scope="session")
def app():
    _app.testing = True

    return _app


@pytest.fixture(scope="function", autouse=True)
def database_clean(app):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()

        yield _db

        _db.session.remove()


@pytest.fixture()
def client(app):
    def _(query={}):
        client = app.test_client()
        return client.post("/graphql", json=query)
    return _

@pytest.fixture()
def add_product(app):
    def _(**kwargs):
        product = Product(**kwargs)
        _db.session.add(product)
        _db.session.commit()
        return product
    return _
