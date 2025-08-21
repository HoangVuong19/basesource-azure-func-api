import os
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = os.environ.get("APP_NAME")
    api_version: str = os.environ.get("API_VERSION")
    api_prefix: str = os.environ.get("API_PREFIX") or "/api/v1"
    algorithms_jwt: str = os.environ.get("ALGORITHMS_JWT")
    environment: Literal["LOCAL", "STAGING", "PRODUCTION"] = (
        os.environ.get("ENVIRONMENT") or "LOCAL"
    )
    database_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    database_username: str = os.environ.get("DATABASE_USERNAME")
    database_password: str = os.environ.get("DATABASE_PASSWORD")
    database_port: str = os.environ.get("DATABASE_PORT")
    database_name: str = os.environ.get("DATABASE_NAME")
    system_log_file: str | None = os.environ.get("SYSTEM_LOG_FILE")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pragma: no cover
