import json
import time
from pathlib import Path


class ClipboardCache:
    DURATION = 120
    PATH = Path.home() / ".cache" / "clipboard_template.json"

    @classmethod
    def get_data(cls) -> dict | None:
        if not cls.PATH.exists():
            return None

        try:
            cache_data = json.loads(cls.PATH.read_text(encoding="utf-8"))
            if time.time() - cache_data["timestamp"] < cls.DURATION:
                return cache_data
        except (json.JSONDecodeError, KeyError, OSError):
            pass

        cls.PATH.unlink(missing_ok=True)
        return None

    @classmethod
    def save(cls, data: str, reason: str) -> None:
        cache_data = {"data": data, "timestamp": time.time(), "reason": reason}
        cls.PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.PATH.write_text(json.dumps(cache_data), encoding="utf-8")

    @classmethod
    def clear(cls) -> None:
        cls.PATH.unlink(missing_ok=True)
