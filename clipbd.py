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

def get_youtube_content():
    result = dict()
    items = get_lastest_clipboard(n=2, include_images=False)
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
        text = item['data'].strip()
        if text := extract_medium(text):
            result["medium_content"] = text
    if "medium_content" in result:
        return result

    raise ValueError("No valid clipboard data.")

from html_to_md import html_to_markdown
def get_webpage():
    result = { "source_url": "Not provided" }
    """ with CopyHTML chrome plugin: get raw html text with CopyHTML plugin. """
    items = get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if text := html_to_markdown(text):
            result["markdown_content"] = text
    if "markdown_content" in result:
        return result

    raise ValueError("No valid clipboard data.")

if __name__ == '__main__':
    print( get_medium() )
    # print( get_youtube_content() )
