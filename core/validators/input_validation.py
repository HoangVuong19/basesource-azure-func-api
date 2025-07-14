from core.validators import BeValidator
from core.validators.errors_validation import StrMaxLenghtError, StrMinLenghtError, StrRequiredError


class InputValidator:
    class String(BeValidator):
        def __init__(self, field_name: str, value: str):
            super().__init__()
            self.field_name = field_name
            self.value = value
            if value is not None:
                self.__len = len(value)
        
        def required(self):
            if not self.value:
                self.value = None
                self.errors.append(StrRequiredError(self.field_name))
            return self
        
        def min_length(self, min_len: int):
            if self.value is not None and self.__len < min_len:
                self.errors.append(StrMinLenghtError(self.field_name, min_len))
            return self
        
        def max_length(self, max_len: int):
            if self.value is not None and self.__len > max_len:
                self.errors.append(StrMaxLenghtError(self.field_name, max_len))
            return self