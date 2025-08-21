from fastapi import APIRouter
from utils.response import response_success

router = APIRouter()


@router.get("/")
def health_check():
    return response_success("Health check good")
