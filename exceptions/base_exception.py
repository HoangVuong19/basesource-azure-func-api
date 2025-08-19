class BaseException(Exception):
    http_code: int | str
    error_code: str
    message: str
    rollback: bool
