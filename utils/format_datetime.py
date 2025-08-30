from datetime import datetime
from zoneinfo import ZoneInfo

from configs.env import get_settings

settings = get_settings()


def get_datetime_now():
    """Return current datetime with timezone info"""
    return datetime.now(ZoneInfo(settings.app_timezone)).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )
