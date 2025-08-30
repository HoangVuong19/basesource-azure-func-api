from pydantic import BaseModel, model_validator
from utils.case_convert import to_snake, convert_dict_keys
from typing import Any


class BaseRequestSchema(BaseModel):

    @model_validator(mode='before')
    @classmethod
    def convert_to_snake_case(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return convert_dict_keys(data, to_snake)
        return data