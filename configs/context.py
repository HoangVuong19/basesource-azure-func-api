import uuid
from contextvars import ContextVar

# context variable, used in multi-thread request
request_id: ContextVar[uuid.UUID] = ContextVar(
    "request_id", default=uuid.UUID("00000000-0000-0000-0000-000000000000")
)
