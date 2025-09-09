#!/usr/bin/env python3
"""Data type detection for clipboard content."""

import re
from enum import Enum
from typing import Any
from ck_clipboard import get_clipboard_data, ClipboardData
from text_info2 import get_text_type


class Datatype(Enum):
    YOUTUBE = "youtube"
    WEBURL = "webpage"
    HTML_TEXT = "html_text"
    MARKDOWN = "markdown"
    LONGTEXT = "longtext"
    IMAGE = "image"


def is_url(string: str) -> bool:
    """Check if string is a valid HTTP/HTTPS URL."""
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.match(pattern, string) is not None


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube video."""
    return ('youtube.com/watch' in url) or ('youtu.be/' in url)


def get_clipboard() -> tuple[Datatype, str|Any] | None:
    """
    Get clipboard data and return the detected Datatype.

    Returns:
        Datatype | None: Detected content type or None if no clipboard data
    """
    data = get_clipboard_data()

    if not data:
        return None

    if data.type == 'image':
        return Datatype.IMAGE, data.data

    if data.type == 'text':
        dtype = None
        text_data = str(data.data)

        # Check if it's a URL
        if is_url(text_data):
            if is_youtube_url(text_data):
                dtype = Datatype.YOUTUBE
            else:
                dtype = Datatype.WEBURL

        # For longer text content, analyze the format
        elif len(text_data) >= 300:
            text_type, details = get_text_type(text_data)

            if text_type == "html":
                dtype = Datatype.HTML_TEXT
            elif text_type == "markdown":
                dtype = Datatype.MARKDOWN
            else:
                dtype = Datatype.LONGTEXT

        if dtype is not None:
            return (dtype, text_data)

    return None


if __name__ == "__main__":
    # Test the function
    dtype = get_clipboard()
    if dtype:
        dtype, text_data = dtype
        print(f"Clipboard content type: {dtype}, {len(text_data)}")
    else:
        print("No clipboard data or unrecognized type")


