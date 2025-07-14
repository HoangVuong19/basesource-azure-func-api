from api.healthcheck import healthcheck_app, healthcheck_route

from core.utils.application import create_fastapi


def test_app():
    testApp = create_fastapi()
    testApp.mount(healthcheck_route, healthcheck_app)

    return testApp
