from exceptions.exam_exception import ExamException
from utils.messages import load_messages

messages = load_messages()


class AppException(ExamException):
    def __init__(self, key: str, rollback: bool = False):
        message_info = messages.get(key, {})
        self.http_code = message_info.get("http_code", 200)
        self.error_code = message_info.get("error_code", key)
        self.message = message_info.get("message", "An error occurred")
        self.rollback = rollback


class InvalidSession(AppException):
    def __init__(self):
        super().__init__("INVALID_SESSION")


class ResourceNotFound(AppException):
    def __init__(self):
        super().__init__("RESOURCE_NOT_FOUND")
