import subprocess, json

def clear_lastest_clipboard(n=3):
    text_cmd = ["copyq", "remove", *map(str, range(n))]
    return subprocess.run(text_cmd, capture_output=True, check=True)


def copyq_read(row):
    script = f"""
        var plain_text = str(read('text/plain', {row}));
        var ts   = str(read('application/x-copyq-timestamp', {row}));
        JSON.stringify({{text: plain_text, timestamp: ts}})
    """
    out = subprocess.run( ["copyq", "eval", script], capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip())

def get_lastest_clipboard(n, debug=False):
    """Get latest clipboard items including text and optionally images.

    Args:
        n: Number of clipboard items to retrieve
        include_images: Whether to include image data

    Returns:
        List of dicts with 'type' and 'data' keys
    """
    items = []

    for i in range(n):
        try:
            text_data = copyq_read(i)

            if text_data:
                ts = datetime.strptime(text_data['timestamp'], '%Y-%m-%d %H:%M:%S')
                elapsed = (datetime.now() - ts).total_seconds()
                if elapsed > 60: continue # skip, too old
                items.append({
                    'type': 'text',
                    'data': text_data['text'],
                })
                continue
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            pass

    if debug:
        for i, item in enumerate(items, start=1):
            print(f"{i}: {item}")
    return items


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
