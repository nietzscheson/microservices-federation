from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import Settings


class MainContainer(containers.DeclarativeContainer):

    settings = providers.Configuration(pydantic_settings=[Settings()])

    engine = providers.Singleton(
        create_engine,
        settings.database_url,
    )

    session = providers.Singleton(
        sessionmaker,
        bind=engine,
        expire_on_commit=False,
    )
