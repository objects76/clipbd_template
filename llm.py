import subprocess
import shlex
import locale
import time

def wait_page_loaded(needle, timeout=3):
    cmds = "xdotool search --name --class microsoft-edge"

    result = subprocess.run(cmds.split(), capture_output=True, text=True, timeout=timeout)
    window_ids = [w for w in result.stdout.strip().split('\n') if w]

    for window_id in window_ids:
        print('activate: ', window_id)
        result = subprocess.run(['xdotool', 'windowactivate', window_id], capture_output=True, text=True, check=True, timeout=timeout)
        if result.returncode == 0 and not result.stderr.strip():
            print('windowactivate: ', result)

            result = subprocess.run(['xdotool', 'getwindowname', window_id], capture_output=True, text=True, check=True, timeout=timeout)
            if result.returncode == 0:
                title = result.stdout.strip()
                print('getwindowname: ', title)
                if needle.lower() in title.lower():
                    print('page loaded: ', title)
                    return True
    return False


def run_web_llm(profile: str, url: str, wait_title:str="chatgpt") -> None:
    """Launch browser with sanitized inputs.

    Args:
        user (str): Browser profile directory name
        url (str): URL to open
    """
    BROWSER = "microsoft-edge-stable"

    # Sanitize inputs to prevent command injection
    safe_user = shlex.quote(profile)
    safe_url = shlex.quote(url)
    args = [
        BROWSER,
        f"--profile-directory={safe_user}",
        "--new-tab",
        safe_url
    ]
    subprocess.Popen(args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True)

    wait_page_loaded(wait_title, 3)
    time.sleep(1)