from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs.env import get_settings
from exceptions.app_exception import AppException
from exceptions.handler import app_exception_handler
from exceptions.handler import system_exception_handler
from exceptions.system_exception import SystemException
from middlewares.auth_middleware import AuthMiddleware
from middlewares.db_session_middleware import DatabaseSessionMiddleware
from middlewares.request_logging_middleware import RequestLoggingMiddleware

settings = get_settings()


def create_fastapi() -> FastAPI:
    fastapi_params = {
        "title": settings.app_name,
        "version": settings.api_version,
    }

    app = FastAPI(**fastapi_params)

    # add all exception handlers of the app
    __EXCEPTION_HANDLERS__ = [
        (AppException, app_exception_handler),
        (SystemException, system_exception_handler),
    ]

    for exc, handler in __EXCEPTION_HANDLERS__:
        app.add_exception_handler(exc, handler)

    # add middlewares
    __MIDDLEWARES__ = [
        AuthMiddleware,
        RequestLoggingMiddleware,
        DatabaseSessionMiddleware,
    ]

    for middleware in __MIDDLEWARES__.__reversed__():
        app.add_middleware(middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
