from core.validators.errors_validation import CommonValidationError


class BeValidator:
    errors: list[CommonValidationError]

    def __init__(self):
        self.errors = []
    
    def get_errors(self) -> list[CommonValidationError]:
        return self.errors
