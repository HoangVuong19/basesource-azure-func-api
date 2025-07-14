import azure.functions as func
from fastapi import FastAPI

from core.configs.env import get_settings
from api.healthcheck import healthcheck_app, healthcheck_route

app = func.FunctionApp()
settings = get_settings()


def register_api(
    fast_app: FastAPI,
    func_name: str,
    route_prefix: str,
    auth_level: func.AuthLevel = func.AuthLevel.ANONYMOUS,
):
    """Register fastapi api to Azure functions"""

    @app.function_name(func_name)
    @app.route(
        route=route_prefix + "/{*route}",
        auth_level=auth_level,
        methods=[
            func.HttpMethod.GET,
            func.HttpMethod.POST,
            func.HttpMethod.PUT,
            func.HttpMethod.PATCH,
            func.HttpMethod.DELETE,
            func.HttpMethod.OPTIONS,
        ],
    )
    async def _(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        return await func.AsgiMiddleware(fast_app).handle_async(req, context)


# Register api
register_api(healthcheck_app, "healthcheck", healthcheck_route)
