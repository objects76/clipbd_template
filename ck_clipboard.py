import subprocess
import copykitten
import time
from dataclasses import dataclass

@dataclass
class ClipboardData:
    type: str
    data: str | tuple[bytes, int, int]
    timestamp: str = ""

def set_clipboard_data(text: str) -> None:
    copykitten.copy(text)

def _get_clipboard_data() -> ClipboardData | None:
    try:
        text = copykitten.paste()
        if len(text) > 0:
            return ClipboardData(type="text", data=text.strip())
    except copykitten.CopykittenError as e:
        print('text:', e)

    try:
        pixels, width, height = copykitten.paste_image()
        return ClipboardData(type="image", data=(pixels, width, height))
    except copykitten.CopykittenError as e:
        print('image:', e)
    return None


def get_clipboard_data() -> ClipboardData | None:
    data = _get_clipboard_data()
    if data is None:
        time.sleep(1.5)
        data = _get_clipboard_data()

    return data

def clear_clipboard() -> None:
    copykitten.clear()

def paste(return_key: bool = False) -> None:
    time.sleep(0.3)
    args = ['xdotool', 'key', '--clearmodifiers', 'ctrl+v']
    if return_key:
        args.append('Return')

    subprocess.run(args, check=False)

if __name__ == "__main__":
    BROWSER = "microsoft-edge-stable"
    subprocess.run([
        BROWSER,
        f"--profile-directory=Default",
        "--new-tab",
        "https://www.chatgpt.com"
    ], check=False)
    time.sleep(1.5)

    paste(return_key=False)
