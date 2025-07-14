from fastapi import FastAPI
from core.configs.env import get_settings
from core.utils.response import response_success
from core.utils.application import create_fastapi

settings = get_settings()

route: str = f"{settings.api_prefix}/healthcheck"
app: FastAPI = create_fastapi(route)


@app.get("/")
def health_check():
    return response_success("Health check is ok")
