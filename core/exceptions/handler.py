from core.configs.logging_conf import logger
from core.exceptions.app_exception import AppException
from core.exceptions.system_exception import SystemException
from core.utils.response import response_fail


async def app_exception_handler(_, exc: AppException):
    logger.exception(">>>>>> App exception")

    return response_fail(exc)


async def system_exception_handler(_, exc: SystemException):
    logger.exception(">>>>>> System exception")

    return response_fail(exc)
