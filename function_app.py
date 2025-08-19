import azure.functions as func

from api.healthcheck.healthcheck_controller import router as healthcheck_router
from utils.application import create_fastapi

app = func.FunctionApp()

main_fastapi_app = create_fastapi()
main_fastapi_app.include_router(
    healthcheck_router, prefix="/api/healthcheck", tags=["REST"]
)


@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await func.AsgiMiddleware(main_fastapi_app).handle_async(req, context)
