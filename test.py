import subprocess, json, re

def copyq_item(row=0):
    script = f"""
        var text = str(read('text/plain', {row}));
        var ts   = str(read('application/x-copyq-timestamp', {row}));
        JSON.stringify({{text: text, timestamp: ts}})
    """
    out = subprocess.run(
        ["copyq", "eval", script],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    return json.loads(out)


if __name__ == "__main__":
    from rich import print
    print(copyq_item(0))

