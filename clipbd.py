#!/usr/bin/env python3
import subprocess
import sys
import re

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
    items = get_lastest_clipboard(n=3, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data']
        if ('youtube.com/watch' in text or 'youtu.be/' in text) and len(text) < 100:
            result['video_id'] = re.search(r'(?:v=|youtu\.be/)([^&?]+)', text).group(1) if re.search(r'(?:v=|youtu\.be/)([^&?]+)', text) else text
        elif len(text) > 300:
            timestamps = re.findall(r'\n\d+:\d+\n', text)
            if len(timestamps) > 10:
                result['transcript'] = text
    if result.get('video_id') and result.get('transcript'):
        return result

    raise ValueError("No valid clipboard data for youtube.")

def get_prompt():
    result = dict()
    items = get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            return {"prompt": text}

    raise ValueError("No valid clipboard data for youtube.")

if __name__ == '__main__':
    result = get_youtube_content()
    print(result)
