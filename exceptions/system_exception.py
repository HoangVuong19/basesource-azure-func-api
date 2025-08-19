from exceptions.base_exception import BaseException
from utils.messages import load_messages

messages: dict = load_messages()


class SystemException(BaseException):

    def __init__(self, error_code: str = "SYSTEM_ERROR", rollback: bool = True):
        self.http_code = 500
        self.error_code = error_code
        self.message = messages["SYSTEM_EXCEPTION"].get(error_code, "System error occurred!")
        self.rollback = rollback

class DBOperationalError(SystemException):
    def __init__(self):
        super().__init__("DB_OPERATIONAL")
