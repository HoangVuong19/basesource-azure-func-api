import logging

from configs.context import request_id
from configs.env import get_settings


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)

        if record:
            s = s.replace("\r\n", "").replace("\n", "")
        return s


class ContextFilter(logging.Filter):
    """ "Provides request id parameter for the logger"""

    def filter(self, record):
        record.request_id = request_id.get()
        return True


# common formatter
formatter = OneLineExceptionFormatter(
    "%(asctime)-15s - %(request_id)s - %(name)-5s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s"
)

# root logger
logger = logging.getLogger("app.fastapi")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addFilter(ContextFilter())

# sql logger
sql_logger = logging.getLogger("sqlalchemy.engine.Engine")
sql_logger.setLevel(logging.INFO)

sql_logger.addHandler(console_handler)
sql_logger.addFilter(ContextFilter())

settings = get_settings()
# log to file if local
if settings.environment == "LOCAL":
    file_handler = logging.FileHandler(settings.system_log_file, "w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addFilter(ContextFilter())

    sql_logger.addHandler(file_handler)
    sql_logger.addFilter(ContextFilter())

# stop delegate logs to root logger (avoid duplicate logs)
sql_logger.propagate = 0
logger.propagate = 0
