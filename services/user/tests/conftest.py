import subprocess
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from src.database import Base
from src.app import app, User
from src.containers import MainContainer


@pytest.fixture
def main_container():

    container = MainContainer()

    return container


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    subprocess.run(["uv", "run", "alembic", "upgrade", "head"])
    yield


@pytest.fixture(autouse=True)
def db(main_container, apply_migrations):
    session_factory = main_container.session()

    with session_factory() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
        session.commit()

        yield session

        session.rollback()


@pytest.fixture()
def client():
    test_client = TestClient(app)

    def _(query={}):
        return test_client.post("/graphql", json=query)
    return _


@pytest.fixture()
def add_user(db):
    def _(**kwargs):
        user = User(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return _
