import subprocess, json
from datetime import datetime
import pyperclip

OLD_CLIPBOARD_THRESHOLD = 0  # Threshold disabled (was 20 seconds)

class CopyQError(Exception):
    pass


def clear_lastest_clipboard(n=3):
    """Clear the latest n clipboard items from CopyQ.

    Args:
        n (int): Number of items to remove from clipboard history

    Returns:
        subprocess.CompletedProcess: Result of the remove operation
    """
    text_cmd = ["copyq", "remove", *map(str, range(n))]
    return subprocess.run(text_cmd, capture_output=True, check=True, timeout=10)



def copyq_read(row: int) -> dict:
    """Read clipboard item at specified row from CopyQ.

    Args:
        row (int): Row number to read (0-based index)

    Returns:
        dict: Contains 'text' and 'timestamp' keys

    Raises:
        subprocess.CalledProcessError: If CopyQ command fails
        json.JSONDecodeError: If response is not valid JSON
    """
    script = f"""
        var plain_text = str(read('text/plain', {row}));
        var ts   = str(read('application/x-copyq-timestamp', {row}));
        JSON.stringify({{text: plain_text, timestamp: ts}})
    """
    try:
        out = subprocess.run(
            ["copyq", "eval", script],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        ).stdout
        return json.loads(out.strip())
    except Exception as e:
        if row == 0:
            return {"text": pyperclip.paste(), "timestamp": ""}
        raise



def get_lastest_clipboard(n: int) -> list[dict]:
    """Get latest clipboard items from CopyQ.

    Args:
        n (int): Number of clipboard items to retrieve
        debug (bool): Enable debug output

    Returns:
        list[dict]: List of clipboard items with 'type' and 'data' keys

    Raises:
        CopyQError: If no valid clipboard items found or all items too old
    """
    items = []
    last_exception = None
    for i in range(n):
        try:
            text_data = copyq_read(i)

            if text_data:
                if OLD_CLIPBOARD_THRESHOLD > 0:
                    ts = datetime.strptime(text_data['timestamp'], '%Y-%m-%d %H:%M:%S')
                    elapsed = int((datetime.now() - ts).total_seconds())
                    # Skip items older than 1 minutes to avoid stale content
                    if elapsed > OLD_CLIPBOARD_THRESHOLD:
                        print(f"Skipping item {i}: too old ({elapsed}s)")
                        continue
                items.append({
                    'type': 'text',
                    'data': text_data['text'],
                })
        except (CopyQError, subprocess.CalledProcessError, UnicodeDecodeError) as e:
            last_exception = e

    if len(items):
        return items


    raise last_exception or CopyQError("No items")

import pyperclip
if __name__ == "__main__":
    from rich import print
    clipbds = copyq_read(0)
    print(clipbds)