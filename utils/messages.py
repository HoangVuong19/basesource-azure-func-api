from functools import lru_cache
import json
import os
import logging

logger = logging.getLogger(__name__)


@lru_cache
def load_messages() -> dict[str, any]:
    """
    Load message definitions from messages.json file.
    This is the single source of truth for all error codes and messages.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        messages_path = os.path.join(current_dir, "../resources/messages.json")

        with open(messages_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load messages.json: {str(e)}")
        return {}
