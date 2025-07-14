import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.configs.context import request_id
from core.configs.logging_conf import logger
from core.exceptions.app_exception import AppException
from core.exceptions.system_exception import SystemException
from core.utils.response import response_fail


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # unique id for each request
        request_id.set(uuid.uuid4())

        logger.info(">>>>>> Start request")
        try:
            return await call_next(request)
        except AppException as e:
            return response_fail(e)
        except Exception:
            logger.exception("")
            return response_fail(SystemException())
        finally:
            logger.info(">>>>>> End request")
