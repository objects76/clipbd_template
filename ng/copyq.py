from __future__ import annotations

import subprocess
import json
from datetime import datetime
from typing import Literal
import pyperclip

OLD_CLIPBOARD_THRESHOLD = 0  # Threshold disabled (was 20 seconds)

class CopyQError(Exception):
    pass


def clear_clipboard(indices: list[int] | int):
    """Clear the latest n clipboard items from CopyQ.

    Args:
        n (int): Number of items to remove from clipboard history

    Returns:
        subprocess.CompletedProcess: Result of the remove operation
    """
    indices_list = indices if isinstance(indices, list) else [indices]
    text_cmd = ["copyq", "remove", *map(str, indices_list)]
    return subprocess.run(text_cmd, capture_output=True, check=True, timeout=10)



def copyq_read(row: int = 0) -> dict[str, str]:
    """Read clipboard item at specified row from CopyQ with format detection.

    Args:
        row (int): Row number to read (0-based index)

    Returns:
        dict: Contains data and metadata based on detected format

    Raises:
        subprocess.CalledProcessError: If CopyQ command fails
        json.JSONDecodeError: If response is not valid JSON
    """
    script = f"""
        if (hasClipboardFormat("text/plain")) {{
            var text = str(read('text/plain', {row}));
            var ts = str(read('application/x-copyq-timestamp', {row}));
            tab("plain-text-history");
            add(text);
            JSON.stringify({{type: "text", data: text, timestamp: ts}});
        }} else if (hasClipboardFormat("image/png")) {{
            var img = str(read('image/png', {row}));
            var ts = str(read('application/x-copyq-timestamp', {row}));
            tab("image-history");
            add(img);
            JSON.stringify({{type: "image", data: img, timestamp: ts}});
        }} else {{
            var fallback = str(read({row}));
            var ts = str(read('application/x-copyq-timestamp', {row}));
            JSON.stringify({{type: "unknown", data: fallback, timestamp: ts}});
        }}
    """

    try:
        out = subprocess.run(
            ["copyq", "eval", script],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        ).stdout
        result = json.loads(out.strip())
        return result
    except Exception as e:
        if row == 0:
            return {"type": "text", "data": pyperclip.paste(), "timestamp": ""}
        raise



def get_lastest_clipboard(n: int) -> list[dict[str, str]]:
    """Get latest clipboard items from CopyQ.

    Args:
        n (int): Number of clipboard items to retrieve

    Returns:
        list[dict]: List of clipboard items with 'type' and 'data' keys

    Raises:
        CopyQError: If no valid clipboard items found or all items too old
    """
    items = []
    last_exception = None
    for i in range(n):
        try:
            clip_data = copyq_read(i)

            if clip_data and clip_data.get('data'):
                if OLD_CLIPBOARD_THRESHOLD > 0 and clip_data.get('timestamp'):
                    ts = datetime.strptime(clip_data['timestamp'], '%Y-%m-%d %H:%M:%S')
                    elapsed = int((datetime.now() - ts).total_seconds())
                    if elapsed > OLD_CLIPBOARD_THRESHOLD:
                        print(f"Skipping item {i}: too old ({elapsed}s)")
                        continue
                items.append({
                    'type': clip_data['type'],
                    'data': clip_data['data'],
                })
        except (CopyQError, subprocess.CalledProcessError, UnicodeDecodeError) as e:
            last_exception = e

    if len(items):
        return items

    raise last_exception or CopyQError("No items")

if __name__ == "__main__":
    from rich import print
    clipbds = copyq_read(0)
    print(clipbds)