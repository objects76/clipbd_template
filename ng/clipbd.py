#!/usr/bin/env python3


from ck_clipboard import ClipboardData
from exceptions import ContentNotFoundError, WebExtractionError


def get_webpage(url: str):
    """with CopyHTML chrome plugin: get raw html text with CopyHTML plugin."""
    items = [ClipboardData(type="text", data=url)]
    for i, item in enumerate(items, start=1):
        if item.type != "text":
            continue
        url = str(item.data).strip() if isinstance(item.data, str) else ""
        if not url.startswith("https:") and not url.startswith("http:"):
            continue
        text_format, text_content = crawling(url)
        return {
            "source_url": url,
            "content_format": text_format,
            "content_text": text_content,
        }

    raise WebExtractionError("No valid web URL found in clipboard data")


def get_longtext(text=None):
    result = {"source_url": "Not provided"}
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """

    if text:
        text = [ClipboardData(type="text", data=text)]

    items = text or get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item.type != "text":
            continue
        long_text = str(item.data).strip() if isinstance(item.data, str) else ""
        if len(long_text) > 500:
            result["content_format"] = "text"
            result["content_text"] = long_text

    if "content_text" in result:
        return result
    raise ContentNotFoundError(
        "No long text content found in clipboard (minimum 500 characters required)"
    )


if __name__ == "__main__":
    pass
    # print( get_webpage('https://news.hada.io/topic?id=22490') )
    # print( get_medium() )
    # print( get_youtube_content('https://www.youtube.com/watch?v=FI7huMLcIrM') )
