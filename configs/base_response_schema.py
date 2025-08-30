import humps
from datetime import datetime
from pydantic import BaseModel, field_serializer, ConfigDict


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=humps.camelize,
        populate_by_name=True,
    )

    @field_serializer("*", when_used="json")
    def serialize_datetime(self, v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        return v
