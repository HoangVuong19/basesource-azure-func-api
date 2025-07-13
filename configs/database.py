from typing import TypeVar
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configs.env import get_settings
from sqlalchemy.engine import URL

settings = get_settings()

database_url = URL.create(
    drivername="postgresql",
    host=settings.database_hostname,
    username=settings.database_username,
    password=settings.database_password,
    port=settings.database_port,
    database=settings.database_name,
)

engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
ModelType = TypeVar("ModelType", bound=Base)  # type: ignore


def get_db(request: Request):
    return request.state.db # pragma: no cover


def get_db_session():
    return SessionLocal() # pragma: no cover
