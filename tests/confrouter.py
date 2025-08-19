
from utils.application import create_fastapi
from api.healthcheck.healthcheck_controller import router as healthcheck_router


def test_app():
    testApp = create_fastapi()
    testApp.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["REST"])

    return testApp
