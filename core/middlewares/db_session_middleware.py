from fastapi import Request
from sqlalchemy.exc import DatabaseError
from starlette.middleware.base import BaseHTTPMiddleware

from core.configs.database import get_db_session
from core.configs.logging_conf import logger
from core.exceptions.system_exception import DBOperationalError
from core.utils.response import response_fail


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(">>>>>>> Start DB session")

        # Declare a db_session for the request
        request.state.db = get_db_session()

        try:
            response = await call_next(request)
            request.state.db.commit()
            return response
        except DatabaseError:
            logger.exception("")
            return response_fail(DBOperationalError())
        finally:
            request.state.db.close()
            logger.info(">>>>>>> End DB session")
