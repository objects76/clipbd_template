#!/usr/bin/env python3
from __future__ import annotations

import os
import shlex
import subprocess
import pyperclip
from pathlib import Path
import sys
import yaml
import ng.clipbd as clipbd
import time
import re
from ng.clipbd import get_lastest_clipboard
from copyq import clear_clipboard
from config import Config
import q_and_a
from exceptions import ClipboardTemplateError
from dunstify import notify_send, notify_cont, notify_close
from text_info2 import get_text_type
import webpage
import youtube
from enum import Enum

rprint = print
VERSION = "1.0.0"

class Commands(Enum):
    SUMMARY = "Summary"
    QA = "Q&A"
    META_PROMPT = "Meta Prompt"
    IMAGE_ANALYSIS = "Image Analysis"

class Subtype(Enum):
    YOUTUBE = "youtube"
    WEBURL = "webpage"
    HTML_TEXT = "html_text"
    MARKDOWN = "markdown"
    LONGTEXT = "longtext"
    IMAGE = "image"

# Configuration from environment
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')


def run_web_llm(profile: str, url: str) -> None:
    """Launch browser with sanitized inputs.

    Args:
        user (str): Browser profile directory name
        url (str): URL to open
    """
    BROWSER = "microsoft-edge-stable"

    # Sanitize inputs to prevent command injection
    safe_user = shlex.quote(profile)
    safe_url = shlex.quote(url)

    subprocess.run([
        BROWSER,
        f"--profile-directory={safe_user}",
        "--new-tab",
        safe_url
    ], check=False)

def resource_path(name: str) -> Path:
    ''' get file path from packed executable '''
    try:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base / name
    except Exception as ex:
        print(ex)
        return Path(name)

def get_template(template_path: str, command: Commands, subtype: Subtype | None) -> str:
    template_yaml = Path(template_path).expanduser()
    if not template_yaml.exists():
        raise ValueError(f'not found: {template_yaml}')

    config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
    templates = config.get('TEMPLATES', {})
    if not isinstance(templates, dict) or not templates:
        raise ValueError('no templates')

    print(f"command: {command}, subtype: {subtype}")

    if command == Commands.SUMMARY:
        assert subtype is not None, "subtype is required"
        if subtype == Subtype.YOUTUBE:
            return templates.get('youtube summary', "")
        elif subtype == Subtype.HTML_TEXT or subtype == Subtype.WEBURL:
            return templates.get('webtext summary', "")
        # elif subtype == Subtype.LONGTEXT:
        #     return templates.get('webpage summary', "")
    elif command == Commands.QA:
        return templates.get('q&a on context', "")
    elif command == Commands.META_PROMPT:
        return templates.get('meta prompt', "")
    elif command == Commands.IMAGE_ANALYSIS:
        return templates.get('image analysis', "")

    raise ValueError(f"Invalid template: {command}, {subtype}")


def is_url(string: str) -> bool:
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.match(pattern, string) is not None

def get_command(text: str, auto: bool = False, data_type: str = 'text') -> tuple[Commands, Subtype | None] | None:
    if auto:
        command = Commands.SUMMARY if data_type == 'text' else Commands.IMAGE_ANALYSIS
    else:
        cmd = [
            'rofi', '-dmenu', '-no-custom',
            '-theme-str', 'window {width: 10%;} entry { enabled: false; }',
            '-p', f'Choose {VERSION}:',
            '-dpi', '192',
            '-lines', str(len(Commands)),
            '-no-fixed-num-lines',
        ]

        rofi = subprocess.run(
            cmd,
            input='\n'.join([cmd.value for cmd in Commands]),
            text=True,
            capture_output=True,
            timeout=30  # Prevent hanging
        )

        choice = (rofi.stdout or '').strip()

        if not choice:
            return None
        command = Commands(choice)

    if data_type == 'image':
        return Commands.IMAGE_ANALYSIS, Subtype.IMAGE
    elif command == Commands.SUMMARY:
        if (is_url(text) and ('youtube.com/watch' in text or 'youtu.be/' in text)):
            return Commands.SUMMARY, Subtype.YOUTUBE
        elif is_url(text):
            return Commands.SUMMARY, Subtype.WEBURL
        else:
            txt_type, stat = get_text_type(text)
            print(f"text_type: {txt_type}, status: {stat}")
            if txt_type == "html":
                return Commands.SUMMARY, Subtype.HTML_TEXT
            elif txt_type == "markdown":
                return Commands.SUMMARY, Subtype.MARKDOWN
            elif txt_type == "plain":
                return Commands.SUMMARY, Subtype.LONGTEXT

        raise ValueError(f"Invalid clipboard data: {text}")
    else:
        return command, None

def main(args) -> int:
    command, subtype = None, None
    try:
        Config(args.template)

        cb_text = ''
        cb_type = 'text'
        items = get_lastest_clipboard(n=1)
        for i, item in enumerate(items, start=1):
            if item['type'] not in ['text', 'image']: continue
            cb_text = item['data'].strip()
            cb_type = item['type']

        if cb_type == 'text' and len(cb_text) < 20 and not is_url(cb_text):
            raise Warning("No valid text:\n "+cb_text)

        cmdinfo = get_command(cb_text, args.auto, cb_type)
        if cmdinfo is None:
            raise Warning("No command found")

        command, subtype = cmdinfo
        template  = get_template(args.template, command, subtype)
        assert template, "template is empty"
        formatted = ""

        notify_send(command.value, subtype.value if subtype else None)
        if command == Commands.SUMMARY:
            assert subtype is not None, "subtype is required"
            if subtype == Subtype.YOUTUBE:
                notify_cont("summary", "youtube content")
                content = youtube.get_youtube_content(cb_text)

            elif subtype == Subtype.HTML_TEXT:
                notify_cont("summary", "html text content")
                content = webpage.from_html_text(cb_text)
                # rprint(f"content: {content}")

            elif subtype == Subtype.WEBURL:
                notify_cont("summary", "weburl content")
                html_text = webpage.get_html(cb_text)
                content = webpage.from_html_text(html_text)

            formatted = template.format( **content )
            print(f"template: {template}")
            print(f"formatted: {formatted}")

        elif command == Commands.QA:
            content = q_and_a.get_QandA(cb_text)
            formatted = template.format( **content )

        elif command == Commands.META_PROMPT:
            content = clipbd.get_prompt()
            formatted = template.format( **content )

        elif command == Commands.IMAGE_ANALYSIS:
            content = {'image_data': cb_text}
            formatted = template.format( **content ) # content will beignored

        if DEBUG:
            print(f'Template choice: {command}, {subtype}')
            print(f'Template length: {len(template)} characters')
            print(f'Formatted output length: {len(formatted)} characters')

        if formatted:
            if args.auto:
                run_web_llm("Default", "https://www.chatgpt.com")
                time.sleep(1)

            pyperclip.copy(formatted)
            if command == Commands.IMAGE_ANALYSIS:
                subprocess.run(['copyq', 'paste'], check=False) # paste template to chatgpt
                subprocess.run(['copyq', 'select', '1'], check=False) # paste image to chatgpt
                subprocess.run(['copyq', 'paste'], check=False)
                if Config.clear_generated:
                    clear_clipboard(1)
            else:
                time.sleep(0.3)
                if args.auto:
                    subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v', 'Return'], check=False)
                else:
                    subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], check=False)
                if Config.clear_generated:
                    clear_clipboard(0)
        notify_close()
        return 0

    except Warning as e:
        notify_send("Warning", str(e), timeout_ms=1000)
        return 1
    except Exception as e:
        error_msg = f"{command}, {subtype}: {str(e)}"
        if len(error_msg) > 250:
            error_msg = error_msg[:100]+'\n...\n'+error_msg[-100:]
        subprocess.run(["notify-send", "-u", "critical", "Template Error", error_msg], check=False)
        return 1

def test():
    pyperclip.copy("image prompt is here")

    # subprocess.run(['copyq', 'select', '0'], check=False)
    result = subprocess.run(['copyq', 'paste'], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print(f"stderr: {result.stderr}")
    else:
        print(f"Command succeeded. stdout: {result.stdout}")
    # time.sleep(1)
    # clear_lastest_clipboard(n=1)

    subprocess.run(['copyq', 'select', '1'], check=False)
    subprocess.run(['copyq', 'paste'], check=False)
    exit(0)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', '-t', help='Template file path', default='~/.config/rofi/template.yaml')
    parser.add_argument('--auto', '-a', help='Auto select template', action='store_true')
    parser.add_argument('--test', '-x', help='Test script', action='store_true')
    args = parser.parse_args()

    if args.test:
        import time
        for i in range(5, 0, -1):
            print(f"Waiting {i} seconds...")
            time.sleep(1)
        test()

    sys.exit(main(args))
