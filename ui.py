import subprocess


def toast(msg: str):
    cmds = ["notify-send", "-u", "normal", "Information", msg]
    subprocess.run(cmds, check=False)  # noqa: S603


def error(msg: str):
    cmds = ["notify-send", "-u", "critical", "Error", msg]
    subprocess.run(cmds, check=False)  # noqa: S603
