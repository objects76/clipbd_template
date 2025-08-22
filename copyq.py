import subprocess, json
from datetime import datetime
from get_browser_url import get_current_browser_url

OLD_CLIPBOARD_THRESHOLD = 20 # 1min

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
    out = subprocess.run(
        ["copyq", "eval", script],
        capture_output=True,
        text=True,
        check=True,
        timeout=10
    ).stdout
    return json.loads(out.strip())


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

    # if last_exception is None:
    #     active_url = get_current_browser_url()
    #     if active_url:
    #         return [{
    #             'type': 'text',
    #             'data': active_url,
    #         }]

    raise last_exception or CopyQError("No items")


if __name__ == "__main__":
    from rich import print
    s1 = '2025-08-21 15:07:45'
    s2 = '2025-08-21 23:07:45'

    from datetime import datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Current time: {current_time}")

    dt1 = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    dt2 = datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    elapsed = (datetime.now() - dt1).total_seconds()
    print (f"{s1 < s2=}, {elapsed=}")
