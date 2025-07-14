from fastapi.testclient import TestClient
import transaction
from sqlalchemy.orm import Session, close_all_sessions, scoped_session, sessionmaker

from core.configs.database import Base
from core.middlewares import db_session_middleware
from tests.confrouter import test_app
from tests.conftest import engine


class BaseTestCase:
    client: TestClient
    db: Session

    def setup_method(self, method) -> None:
        # Generate DB session
        Base.metadata.create_all(engine)
        self.db = scoped_session(sessionmaker(engine))
        transaction.commit()
        db_session_middleware.get_db_session = lambda: self.db
        self.client = TestClient(test_app())

    def teardown_method(self, method) -> None:
        close_all_sessions()
        Base.metadata.drop_all(engine)
