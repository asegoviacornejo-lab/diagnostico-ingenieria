from __future__ import annotations

import json
from pathlib import Path

from utils.helpers import merge_with_defaults


DATA_DIR = Path(__file__).resolve().parent
USER_DATA_FILE = DATA_DIR / "user_data.json"


def load_user_data() -> dict | None:
    if not USER_DATA_FILE.exists():
        return None

    try:
        with USER_DATA_FILE.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except (json.JSONDecodeError, OSError):
        return None

    return merge_with_defaults(payload)


def save_user_data(data: dict) -> None:
    USER_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = merge_with_defaults(data)
    with USER_DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)
