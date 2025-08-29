import subprocess
import copykitten

# copykitten.copy("The kitten says meow")
# text = copykitten.paste()
# print(f"`{text}`")

def get_clipboard_data():

    try:
        text = copykitten.paste()
        print(f"Size of pixels: {len(text)=}, {text}")
        if len(text) > 0:
            return "text", text
    except copykitten.CopykittenError as e:
        print('text:', e)

    try:
        pixels, width, height = copykitten.paste_image()
        print(type(pixels), f"{width} x {height}")
        print(f"Size of pixels: {len(pixels)} bytes")
        return "image", (pixels, width, height)
    except copykitten.CopykittenError as e:
        print('image:', e)

    return None

def paste_to_ui(second_text: str = "", return_key: bool = False):
    subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], check=False)

    if second_text:
        copykitten.copy(second_text)
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], check=False)

    if return_key:
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'Return'], check=False)

    # copykitten.copy(data)


if __name__ == "__main__":
    import time
    BROWSER = "microsoft-edge-stable"
    subprocess.run([
        BROWSER,
        f"--profile-directory=Default",
        "--new-tab",
        "https://www.chatgpt.com"
    ], check=False)
    time.sleep(1.5)

    paste_to_ui("second text data",return_key=False)
