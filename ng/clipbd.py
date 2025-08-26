#!/usr/bin/env python3
import subprocess
import sys
import re
import json

from bs4 import BeautifulSoup
from youtube import get_youtube_videoid, download_transcript
from copyq import get_lastest_clipboard
from medium import extract_medium
from exceptions import YouTubeExtractionError, ContentNotFoundError, WebExtractionError
from webpage import html_to_md
from config import Config

def get_prompt():
    items = get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            return { "source_prompt": text }

    raise ValueError("No valid clipboard data for youtube.")



def get_webpage(test_url = None):
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """
    if test_url:
        test_url = [{'type': 'text', 'data': test_url}]

    items = test_url or get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        url = item['data'].strip()
        if not url.startswith('https:') and not url.startswith('http:'):
            continue
        text_format, text_content = crawling(url)
        return {
            "source_url": url,
            "content_format": text_format,
            "content_text": text_content,
        }

    raise WebExtractionError(f"No valid web URL found in clipboard data")


def get_longtext(text=None):
    result = { "source_url": "Not provided" }
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """

    if text:
        text = [{'type': 'text', 'data': text}]

    items = text or get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        long_text = item['data'].strip()
        if len(long_text) > 500:
            result["content_format"] = 'text'
            result["content_text"] = long_text

    if "content_text" in result:
        return result
    raise ContentNotFoundError("No long text content found in clipboard (minimum 500 characters required)")


if __name__ == '__main__':
    from rich import print
    # print( get_webpage('https://news.hada.io/topic?id=22490') )
    # print( get_medium() )
    # print( get_youtube_content('https://www.youtube.com/watch?v=FI7huMLcIrM') )
