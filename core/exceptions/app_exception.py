from core.exceptions.base_exception import BaseException
from core.utils.messages import load_messages

messages = load_messages()


class AppException(BaseException):
    def __init__(self, error_code: str, rollback: bool = False):
        self.http_code = 200
        self.error_code = error_code
        self.message = messages["APP_EXCEPTION"].get(error_code, "Application error")
        self.rollback = rollback


class ResourceNotFound(AppException):
    def __init__(self):
        super().__init__("RESOURCE_NOT_FOUND")


class Unauthorized(AppException):
    def __init__(self):
        super().__init__("UNAUTHORIZED")


class DecodeError(AppException):
    def __init__(self):
        super().__init__("DECODE_ERROR")

class ConflictError(AppException):
    def __init__(self):
        super().__init__("CONCURRENCY_CONFLICT_ERROR")
