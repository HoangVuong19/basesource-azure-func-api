from sqlalchemy import Boolean, Column, DateTime, String, event

from configs.database import Base
from utils import format_datetime


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, nullable=False)
    created_by = Column(String(255))
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(String(255))


class SoftDeleteMixin(Base):
    __abstract__ = True

    del_flag = Column(Boolean, default=False)


@event.listens_for(BaseModel, "before_insert", propagate=True)
def before_insert(mapper, connection, target):
    now = format_datetime.get_datetime_now()

    if hasattr(target, "created_at"):
        target.created_at = now
    if hasattr(target, "updated_at"):
        target.updated_at = now


@event.listens_for(BaseModel, "before_update", propagate=True)
def before_update(mapper, connection, target):
    now = format_datetime.get_datetime_now()

    if hasattr(target, "updated_at"):
        target.updated_at = now
