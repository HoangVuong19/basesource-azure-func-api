from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.configs.env import get_settings
from core.exceptions.app_exception import AppException
from core.exceptions.handler import app_exception_handler
from core.exceptions.handler import system_exception_handler
from core.exceptions.system_exception import SystemException
from core.middlewares.auth_middleware import AuthMiddleware
from core.middlewares.db_session_middleware import DatabaseSessionMiddleware
from core.middlewares.request_logging_middleware import RequestLoggingMiddleware
from core.utils.convert_string import fill_prefix

settings = get_settings()


def create_fastapi(api_route: Optional[str] = None) -> FastAPI:
    fastapi_params = {
        "title": settings.app_name,
        "version": settings.api_version,
    }

    if api_route:
        fastapi_params["root_path"] = fill_prefix(api_route)

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
        RequestLoggingMiddleware,
        DatabaseSessionMiddleware,
        AuthMiddleware,
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
