from sqlalchemy import Column, DateTime, String, func

from configs.database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(String(255))
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    updated_by = Column(String(255))
