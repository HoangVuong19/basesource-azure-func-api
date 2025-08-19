from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from configs.env import get_settings
from configs.logging_conf import logger
from exceptions.app_exception import AppException
from exceptions.system_exception import SystemException
from utils.response import response_fail


settings = get_settings()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Do something for authentication here
        logger.info(">>>>>> Start auth")
        try:
            return await call_next(request)
        except AppException as e:
            return response_fail(e)
        except Exception:
            logger.exception("")
            return response_fail(SystemException())
        finally:
            logger.info(">>>>>> End auth")
