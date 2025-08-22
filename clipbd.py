#!/usr/bin/env python3
import subprocess
import sys
import re
from youtube import get_youtube_videoid, download_transcript

def clear_lastest_clipboard(n=3):
    text_cmd = ["copyq", "remove", *map(str, range(n))]
    return subprocess.run(text_cmd, capture_output=True, check=True)


def get_lastest_clipboard(n=3, include_images=False, debug=False):
    """Get latest clipboard items including text and optionally images.

    Args:
        n: Number of clipboard items to retrieve
        include_images: Whether to include image data

    Returns:
        List of dicts with 'type' and 'data' keys
    """
    items = []

    for i in range(n):
        item = {'type': 'text', 'data': None}

        # First try to get text data
        try:
            text_cmd = ["copyq", "read", str(i)]
            text_result = subprocess.run(text_cmd, capture_output=True, check=True)
            text_data = text_result.stdout.decode("utf-8").strip()

            if text_data:
                item['data'] = text_data
                items.append(item)
                continue
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            pass

        # If no text data and images are requested, try image formats
        if include_images:
            for img_format in ['image/png', 'image/jpeg', 'image/gif', 'image/bmp']:
                try:
                    img_cmd = ["copyq", "read", img_format, str(i)]
                    img_result = subprocess.run(img_cmd, capture_output=True, check=True)

                    if img_result.stdout:
                        item['type'] = 'image'
                        item['format'] = img_format
                        item['data'] = img_result.stdout  # Binary data
                        items.append(item)
                        break
                except subprocess.CalledProcessError:
                    continue

    if debug:
        for i, item in enumerate(items, start=1):
            if item['type'] == 'text':
                print(f"[{i}]: text, {len(item['data'])}, {item['data']}")
            elif item['type'] == 'image':
                ext = item['format'].split('/')[-1]
                filename = f"{i}_clipboard.{ext}"
                with open(filename, 'wb') as f:
                    f.write(item['data'])
                print(f"[{i}]: image, {item['format']}, {len(item['data'])} bytes -> saved as {filename}")
    return items

def get_youtube_content(test_url = None):
    result = dict()
    if test_url:
        test_url = [{'type': 'text', 'data': test_url}]

    items = test_url or get_lastest_clipboard(n=2, include_images=False)
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
                result['transcript'] = f"[Error downloading transcript: {e}]"
        return result

    raise ValueError("No valid clipboard data.")

def get_prompt():
    items = get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            return { "source_prompt": text }

    raise ValueError("No valid clipboard data for youtube.")

def get_QandA():
    items = get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            return { "context": text }

    raise ValueError("No valid clipboard data for youtube.")

from medium import extract_medium
def get_medium():
    result = { "source_url": "Not provided" }
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """
    items = get_lastest_clipboard(n=1, include_images=False)
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

    items = text or get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        long_text = item['data'].strip()
        if len(long_text) > 500:
            result["content_format"] = 'text'
            result["content_text"] = long_text

    if "content_text" in result:
        return result
    raise ValueError("No valid clipboard data.")


from scraping import crawling
def get_webpage(test_url = None):
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """
    if test_url:
        test_url = [{'type': 'text', 'data': test_url}]

    items = test_url or get_lastest_clipboard(n=1, include_images=False)
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

    url = url or "No clipboard data"
    raise ValueError(f"No valid clipboard data: {url[:100]}")

if __name__ == '__main__':
    from rich import print
    # print( get_webpage('https://news.hada.io/topic?id=22490') )
    # print( get_medium() )
    # print( get_youtube_content('https://www.youtube.com/watch?v=FI7huMLcIrM') )
