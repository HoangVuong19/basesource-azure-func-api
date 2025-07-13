import logging
import os
import sys

# this is to include backend dir in sys.path so that we can import from main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database

databaseURI = "sqlite:///./tests/api_test.db"

engine = create_engine(databaseURI, echo=True)


def pytest_sessionstart(session):  # pragma: no cover
    """pytest session start"""
    print(" Test session start ")
    if database_exists(databaseURI):
        drop_database(databaseURI)


def pytest_sessionfinish(session):  # pragma: no cover
    """pytest session finish"""
    print(" Test session end ")


@pytest.fixture(autouse=True)
def suppress_sqlalchemy_logs():
    # Suppress SQLAlchemy logs by setting the log level to WARNING or higher
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.ERROR)
