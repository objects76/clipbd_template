#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
import traceback
from pathlib import Path

from ck_clipboard import ClipboardData, clear_clipboard, paste, set_clipboard_data
from command import Command, get_command
from config import Config
from datatype import Datatype, get_clipboard
from dunstify import notify_close, notify_cont, notify_send
from llm import openai_inference, run_web_llm
from prompt import get_prompt
from ui import error, toast

VERSION = "1.0.0"
DEBUG = True


def resource_path(name: str) -> Path:
    """get file path from packed executable"""
    try:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base / name
    except (RuntimeError, ValueError, TypeError) as ex:
        print(ex)
        return Path(name)


def main(args) -> int:
    cb_data = get_clipboard()
    if cb_data is None:
        toast("No clipboard data")
        return 0

    dtype, data = cb_data
    command = get_command(dtype, data)
    if command is None:
        return 0

    try:
        prompt = get_prompt(args.template, command, dtype, data)
        if not prompt:
            notify_send("Error", "No prompt", timeout_ms=1000)
            return 0
    except Exception as e:
        error(str(e))

    Config(args.template)
    try:
        if Config.use_api:
            notify_cont(command.name, "ai processing...")
            result = openai_inference(prompt)
            Path("asset/result.md").write_text(result)
            subprocess.run(["mdviewer.app", "asset/result.md"], check=False)
        else:
            run_web_llm(
                Config.browser_profile, Config.webai, wait_title=Config.webai_title
            )

            if dtype == Datatype.IMAGE:
                paste()  # paste image to chatgpt
                time.sleep(1.5)
            else:
                with Path("/tmp/source.md").open("w", encoding="utf-8") as f:
                    f.write(prompt["content_text"])
                set_clipboard_data(ClipboardData(type="file", data="/tmp/source.md"))
                paste()  # paste text file to chatgpt
                time.sleep(1.5)

            template = prompt.get("template", "")
            print("prompt: ", template[:100])
            set_clipboard_data(
                ClipboardData(type="text", data=template)
            )  # set prompt text to clipboard
            paste(
                return_key=args.auto and command != Command.QA
            )  # paste prompt text to chatgpt

            if Config.clear_generated:
                time.sleep(2)
                clear_clipboard()
                print("clipboard cleared")
            return 0

    except Warning as e:
        notify_send("Warning", str(e), timeout_ms=1000)
        return 1
    except (RuntimeError, ValueError, TypeError) as e:
        if DEBUG:
            print(f"error: {e}")

            traceback.print_exc()

        error_msg = f"{command}: {e!s}"
        if len(error_msg) > 250:
            error_msg = error_msg[:100] + "\n...\n" + error_msg[-100:]
        error(error_msg)
        return 1
    finally:
        notify_close()


def test():
    Config("asset/template2.yaml")

    run_web_llm(Config.browser_profile, Config.webai, wait_title=Config.webai_title)
    sys.exit(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        "-t",
        help="Template file path",
        default="~/.config/rofi/template.yaml",
    )
    parser.add_argument(
        "--auto", "-a", help="Auto select template", action="store_true"
    )
    parser.add_argument("--test", "-x", help="Test script", action="store_true")
    args = parser.parse_args()

    if args.test:
        import time

        for i in range(5, 0, -1):
            print(f"Waiting {i} seconds...")
            time.sleep(1)
        # test()

    sys.exit(main(args))
