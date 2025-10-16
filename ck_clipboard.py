import subprocess
import copykitten
import time
from dataclasses import dataclass
from typing import Literal
import subprocess
import pathlib

def set_clipboard_file_uris(path_list):
    uris = []
    for p in path_list:
        p = pathlib.Path(p).absolute()
        uris.append("file://" + str(p))
    data = "\r\n".join(uris) + "\r\n"
    # Use xclip
    subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "text/uri-list"],
        input=data.encode("utf-8"),
        check=True
    )

ClipboardType = Literal["text", "image", "file"] = Literal["text", "image"]

# xclip -selection clipboard -t x-special/gnome-copied-files
@dataclass
class ClipboardData:
    type: ClipboardType
    data: str | tuple[bytes, int, int] | list[str]
    timestamp: str = ""

def set_clipboard_data(data: ClipboardData) -> None:
    if data.type == "text":
        copykitten.copy(str(data.data))
    elif data.type == "image":
        copykitten.copy_image(*data.data) # type: ignore
    elif data.type == "file":
        set_clipboard_file_uris([data.data]) # type: ignore
    else:
        raise ValueError(f"Unsupported data type: {data.type}")

def _get_clipboard_data(nth=0) -> ClipboardData | None:
    try:
        text = copykitten.paste()
        if len(text) > 0:
            return ClipboardData(type="text", data=text.strip())
    except copykitten.CopykittenError as e:
        print(f'text.{nth}:', e)

    try:
        pixels, width, height = copykitten.paste_image()
        return ClipboardData(type="image", data=(pixels, width, height))
    except copykitten.CopykittenError as e:
        print(f'image.{nth}:', e)
    return None


def get_clipboard_data() -> ClipboardData | None:
    data = _get_clipboard_data()
    if data is None:
        time.sleep(1.5)
        data = _get_clipboard_data(nth=1)

    return data

def clear_clipboard() -> None:
    copykitten.clear()

def paste(return_key: bool = False) -> None:
    time.sleep(0.3)
    args = ['xdotool', 'key', '--clearmodifiers', 'ctrl+v']
    if return_key:
        time.sleep(0.3)
        args.append('Return')

    subprocess.run(args, check=False)


#
# file
#
import locale
import sys, os, subprocess
from six import binary_type
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

if sys.platform.startswith('win'):
    import win32clipboard  # pylint: disable=import-error


def get_clipboard_formats():
    '''
    Return list of all data formats currently in the clipboard
    '''
    formats = []
    if sys.platform.startswith('linux'):
        encoding = locale.getpreferredencoding()
        com = ["xclip", "-o", "-t", "TARGETS"]
        try:
            p = subprocess.Popen(com,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                )
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                for line in stdout.decode(encoding).splitlines():
                    formats.append(line.strip())
        except Exception as e:
            print("Exception from starting subprocess {0}: " "{1}".format(com, e))

    if sys.platform.startswith('win'):
        f = win32clipboard.EnumClipboardFormats(0)
        while f:
            formats.append(f)
            f = win32clipboard.EnumClipboardFormats(f)

    if not formats:
        print("get_clipboard_formats: formats are {}: Not implemented".format(formats))
    else:
        #print(formats)
        return formats

def enum_files_from_clipboard(mime):
    '''
    Generates absolute paths from clipboard
    Returns unverified absolute file/dir paths based on defined mime type
    '''
    paths = []
    if sys.platform.startswith('linux'):
        encoding = locale.getpreferredencoding()
        com = ["xclip", "-selection", "clipboard","-o", mime]
        try:
            p = subprocess.Popen(com,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                )
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                for line in stdout.decode(locale.getpreferredencoding()).splitlines():
                    line = line.strip()
                    # if line.startswith("file://"):
                    #     paths.append(unquote(line.replace("file://", "")))
                    # else:
                    #     paths.append(unquote(line))
                    paths.append(unquote(line))
            return paths
        except Exception as e:
            print("Exception from starting subprocess {0}: " "{1}".format(com, e))

def get_clipboard_files(folders=False):
    '''
    Enumerate clipboard content and return files/folders either directly copied or
    highlighted path copied
    '''
    files = None
    if sys.platform.startswith('win'):
        try:
            win32clipboard.OpenClipboard()
            f = get_clipboard_formats()
            if win32clipboard.CF_HDROP in f:
                files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            elif win32clipboard.CF_UNICODETEXT in f:
                files = [win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)]
            elif win32clipboard.CF_TEXT in f:
                files = [win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)]
            elif win32clipboard.CF_OEMTEXT in f:
                files = [win32clipboard.GetClipboardData(win32clipboard.CF_OEMTEXT)]

            if files:
                if folders:
                    files = [f for f in files if os.path.isdir(f)]
                else:
                    files = [f for f in files if os.path.isfile(f)]
                files = files if files else None

            return files
        except Exception as e:
            print(f"Windows clipboard error: {e}")
            return None
        finally:
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass

    if sys.platform.startswith('linux'):
        f = get_clipboard_formats()
        if "UTF8_STRING" in f:
            files = enum_files_from_clipboard("UTF8_STRING")
        elif "TEXT" in f:
            files = enum_files_from_clipboard("TEXT")
        elif "text/plain" in f:
            files = enum_files_from_clipboard("text/plain")
        if folders:
            files = [f for f in files if os.path.isdir(str(f))] if files else None
        else:
            files = [f for f in files if os.path.isfile(str(f))] if files else None
        return files

#get_clipboard_files(folders=True)

if __name__ == "__main__":

#     BROWSER = "microsoft-edge-stable"
#     subprocess.run([
#         BROWSER,
#         f"--profile-directory=Default",
#         "--new-tab",
#         "https://www.chatgpt.com"
#     ], check=False)
#     time.sleep(1.5)
#
#     paste(return_key=False)

    # print( get_clipboard_files() )
    print( get_clipboard_formats() )