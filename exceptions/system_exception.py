from exceptions.exam_exception import ExamException
from utils.messages import load_messages

messages: dict = load_messages()


class SystemException(ExamException):
    http_code = 500
    error_code = "INTERNAL_SERVER_ERROR"
    message = messages.get(error_code)["message"]
    rollback = True

    def __init__(self, key: str = None, rollback: bool = True):
        if key:
            message_info = messages.get(key, {})
            self.error_code = message_info.get("error_code", "")
            self.message = message_info.get("message", "An error occurred!")
            self.rollback = rollback


class DBOperationalError(SystemException):
    def __init__(self):
        super().__init__("INVALID_SESSION")
