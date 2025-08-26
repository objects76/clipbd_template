#!/usr/bin/env python3
import subprocess
import sys
import re
import json
from youtube import get_youtube_videoid, download_transcript
from copyq import get_lastest_clipboard
from medium import extract_medium
from exceptions import YouTubeExtractionError, ContentNotFoundError, WebExtractionError
from web_to_md import html_to_md

def get_youtube_content(test_url = None):
    result = dict()
    if test_url:
        test_url = [{'type': 'text', 'data': test_url}]

    items = test_url or get_lastest_clipboard(n=2)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data']
        if ('youtube.com/watch' in text or 'youtu.be/' in text) and len(text) < 100:
            result['video_id'] = get_youtube_videoid(text)

        elif len(text) > 300:
            timestamps = re.findall(r'\n\d+:\d+\n', text)
            if len(timestamps) > 10:
                result['transcript'] = text

    if result.get('video_id'):
        if 'transcript' not in result:
            try:
              result['transcript'] = download_transcript(result['video_id'])
            except Exception as e:
                raise YouTubeExtractionError(f"Failed to download transcript for video {result['video_id']}: {e}")
        return result

    raise ContentNotFoundError("No YouTube content found in clipboard")

def get_prompt():
    items = get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            return { "source_prompt": text }

    raise ValueError("No valid clipboard data for youtube.")

def get_medium():
    result = { "source_url": "Not provided" }
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """
    items = get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text_format, text_content = extract_medium( item['data'].strip() )
        result["content_format"] = text_format
        result["content_text"] = text_content

    if "content_text" in result:
        return result

    raise ValueError("No valid clipboard data.")


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


from scraping import crawling

def get_current_browser_url():
    """Get URL from current active browser window."""
    try:
        from get_browser_url import get_current_browser_url as get_url
        return get_url()
    except ImportError:
        # Fallback to simple clipboard method
        import subprocess
        import time
        import pyperclip

        try:
            original_clipboard = pyperclip.paste()
            subprocess.run(['xdotool', 'key', 'ctrl+l'], check=True)
            time.sleep(0.1)
            subprocess.run(['xdotool', 'key', 'ctrl+c'], check=True)
            time.sleep(0.1)
            url = pyperclip.paste().strip()
            pyperclip.copy(original_clipboard)

            if url.startswith(('http://', 'https://')):
                return url
        except Exception as e:
            print(f"Failed to get browser URL: {e}")

        return None

def get_webpage_from_browser():
    """Get webpage content from current browser URL."""
    url = get_current_browser_url()
    if not url:
        raise WebExtractionError("Could not get URL from active browser window")

    text_format, text_content = crawling(url)
    return {
        "source_url": url,
        "content_format": text_format,
        "content_text": text_content,
    }

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

if __name__ == '__main__':
    from rich import print
    # print( get_webpage('https://news.hada.io/topic?id=22490') )
    # print( get_medium() )
    # print( get_youtube_content('https://www.youtube.com/watch?v=FI7huMLcIrM') )
