from core.utils.messages import load_messages


messages = load_messages()

class CommonValidationError:
    def __init__(self, field_name: str, error_code: str, message: str, http_code: int = 200):
        self.field_name = field_name
        self.error_code = error_code
        self.message = message
        self.http_code = http_code

    def to_dict(self):
        return {
            "field_name": self.field_name,
            "error_code": self.error_code,
            "message": self.message
        }

class StrRequiredError(CommonValidationError):
    error_code = "REQUIRED_ERROR"
    msg_template = messages["APP_EXCEPTION"][error_code]
    
    def __init__(self, field_name: str):
        message = self.msg_template.format(field_name=field_name)
        super().__init__(field_name, self.error_code, message)

class StrMinLenghtError(CommonValidationError):
    error_code = "MIN_LEN_ERROR"
    msg_template = messages["APP_EXCEPTION"][error_code]
    
    def __init__(self, field_name: str, min_len: int):
        message = self.msg_template.format(field_name=field_name, min_len=min_len)
        super().__init__(field_name, self.error_code, message)

class StrMaxLenghtError(CommonValidationError):
    error_code = "MAX_LEN_ERROR"
    msg_template = messages["APP_EXCEPTION"][error_code]
    
    def __init__(self, field_name: str, max_len: int):
        message = self.msg_template.format(field_name=field_name, max_len=max_len)
        super().__init__(field_name, self.error_code, message)
