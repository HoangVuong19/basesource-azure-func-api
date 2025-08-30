from datetime import datetime
from http import HTTPStatus

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from exceptions.app_exception import AppException


def serialize_data(data: any) -> any:
    """
    Serialize different types of data to JSON-compatible format.

    Args:
        data (Any): The data to be serialized.

    Returns:
        Any: Serialized data.
    """
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json", by_alias=True)

    if hasattr(data, "__dict__"):
        data_dict: dict[str, any] = data.__dict__
        data = {k: v for k, v in data_dict.items() if not k.startswith("_")}
        return serialize_data(data)
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, (list, tuple)):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(data, (str, int, float, bool, type(None))):
        return data
    else:
        return str(data)


def response_success(data: any):
    return JSONResponse(
        content={"success": True, "data": serialize_data(data), "errors": []},
        status_code=HTTPStatus.OK,
    )


def response_fail(exc: AppException | list[AppException]):
    if isinstance(exc, list):
        errors = [{"code": e.error_code, "message": e.message} for e in exc]
        status_code = exc[0].http_code if exc else HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        errors = [{"code": exc.error_code, "message": exc.message}]
        status_code = exc.http_code

    return JSONResponse(
        content={
            "success": False,
            "data": None,
            "errors": errors,
        },
        status_code=status_code,
    )
