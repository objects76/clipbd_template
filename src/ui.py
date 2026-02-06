import os
from typing import Literal


def dunst(
    title: str,
    level: Literal["information", "question", "warning", "error"],
    msg: str = "",
    timeout_sec: int = 3,
    msgid: int = 1,
):
    cmd = f'dunstify -r {msgid} -i dialog-{level} -t {timeout_sec * 1000} "{title.capitalize()}" "{msg}"'
    os.system(cmd)  # noqa: S605


def dunst_close(msgid: int = 1):
    """Close a notification by its message ID."""
    os.system(f"dunstify --close {msgid}")  # noqa: S605
