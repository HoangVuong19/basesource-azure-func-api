from configs.logging_conf import logger
from exceptions.app_exception import AppException
from exceptions.system_exception import SystemException
from utils.response import response_fail


async def app_exception_handler(_, exc: AppException):
    logger.exception(">>>>>> App exception")

    return response_fail(exc)


async def system_exception_handler(_, exc: SystemException):
    logger.exception(">>>>>> System exception")

    return response_fail(exc)
