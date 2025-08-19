from configs.env import get_settings

settings = get_settings()


def fill_prefix(value: str) -> str:
    """Fill prefix to value"""
    if not value.startswith("/"):
        return f"/{value}"
    return value
