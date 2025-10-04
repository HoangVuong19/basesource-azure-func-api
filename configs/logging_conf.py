import logging
import sys
import os

from configs.context import request_id

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter


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
    "[%(filename)s:%(lineno)s - %(funcName)s()] - " "%(user_id)s - " "%(message)s"
)

# root logger
logger = logging.getLogger("app.fastapi")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# sql logger
sql_logger = logging.getLogger("sqlalchemy.engine.Engine")
sql_logger.setLevel(logging.INFO)
sql_logger.addHandler(console_handler)

conn_str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if conn_str:
    provider = LoggerProvider(
        resource=Resource.create({"service.name": "redb-backend"})
    )
    provider.add_log_record_processor(
        BatchLogRecordProcessor(
            AzureMonitorLogExporter.from_connection_string(conn_str)
        )
    )

    azure_handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
    azure_handler.setFormatter(formatter)

    logger.addHandler(azure_handler)
    sql_logger.addHandler(azure_handler)

logger.addFilter(ContextFilter())
sql_logger.addFilter(ContextFilter())

# stop delegate logs to root logger (avoid duplicate logs)
sql_logger.propagate = 0
logger.propagate = 0
