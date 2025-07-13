from datetime import datetime
from http import HTTPStatus

from fastapi.responses import JSONResponse

from exceptions.exam_exception import ExamException


def serialize_data(data: any) -> any:
    """
    Serialize different types of data to JSON-compatible format.

    Args:
        data (Any): The data to be serialized.

    Returns:
        Any: Serialized data.
    """
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
        content={"success": True, "data": serialize_data(data), "error": None},
        status_code=HTTPStatus.OK,
    )


def response_fail(exc: ExamException):
    return JSONResponse(
        content={
            "success": False,
            "data": None,
            "error": {"code": exc.error_code, "message": exc.message},
        },
        status_code=exc.http_code,
    )
