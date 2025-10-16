
import subprocess
import time
import re

def dbg(*args, **kwargs):
    # print(*args, **kwargs)
    pass

def get_window_class(window_id):
    cmd = ["xprop", "-id", window_id, "WM_CLASS"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    win_class = re.search(r"WM_CLASS\(STRING\) = (.*)", result.stdout)
    return win_class.group(1) if win_class else ""

def get_window_title(window_id):
    result = subprocess.run(['xdotool', 'getwindowname', window_id],
                              capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_active_window():
    result = subprocess.run(['xdotool', 'getactivewindow'],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_url(window_id:str):
    subprocess.run(['xdotool', 'key', '--window', window_id, 'ctrl+l','ctrl+c', "Escape"], check=True)
    # url_result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True, check=True)
    # url = url_result.stdout.strip()
    # return url

def wait_page_loaded(window_id:str, needle:str, timeout=2):
    for _ in range(timeout*10):
        result = subprocess.run(['xdotool', 'getwindowname', window_id], capture_output=True, text=True, check=True)
        if needle in result.stdout.strip():
            dbg('page loaded: ', result.stdout.strip())
            return True
        time.sleep(0.1)
    return False

def get_window_info(window_id:str|None = None):
    window_id = window_id or get_active_window()
    title = get_window_title(window_id)
    wm_class = get_window_class(window_id)
    return title, wm_class

def copy_html_text(window_id:str|None = None):
    window_id = window_id or get_active_window()

    title, wm_class = get_window_info(window_id)
    if "microsoft-edge" in wm_class:
        subprocess.run(['xdotool', 'key', '--window', window_id, 'ctrl+u'], check=True)
        wait_page_loaded(window_id, "view-source:")
        time.sleep(3)
        subprocess.run(['xdotool', 'key', '--window', window_id, 'ctrl+a','ctrl+c','ctrl+w'], check=True)
        # html_text = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True, check=True)
        # return html_text.stdout.strip()
        dbg('html text copied from window', title)
        return True
    return False

def copy_youtube_url(window_id:str|None = None):
    window_id = window_id or get_active_window()
    title, wm_class = get_window_info(window_id)
    if "microsoft-edge" in wm_class and "youtube" in title.lower():
        get_url(window_id)
        dbg('url copied from window', title)
        return True
    return False


def active_window_information():
    window_id = get_active_window()
    title, wm_class = get_window_info(window_id)
    return title, wm_class
