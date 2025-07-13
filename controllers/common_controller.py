from fastapi import APIRouter

from configs.env import get_settings
from utils.response import response_success

common_router = APIRouter()
settings = get_settings()


@common_router.get("/healthcheck")
def health_check():
    return response_success("Health check is ok")
