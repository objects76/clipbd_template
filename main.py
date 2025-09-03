#!/usr/bin/env python3
from __future__ import annotations

import os
import shlex
import subprocess
import pyperclip
from pathlib import Path
import sys
import yaml
from cache import ClipboardCache
import meta_prompt
import ng.clipbd as clipbd
import time
import re

from ck_clipboard import get_clipboard_data, clear_clipboard, paste, set_clipboard_data, ClipboardData
from text_info2 import get_text_type

from config import Config
import q_and_a
from dunstify import notify_send, notify_cont, notify_close
import webpage
from window_utils import copy_html_text, copy_youtube_url
import youtube
from enum import Enum
from exceptions import TemplateNotFoundError, TemplateFormatError, ContentNotFoundError
import locale
from llm import openai_inference, run_web_llm

VERSION = "1.0.0"
DEBUG = True

class Commands(Enum):
    SUMMARY = "Summary"
    QA = "Q&A"
    # META_PROMPT = "Meta Prompt"
    TRANSLATE_TO_KOREAN = "Translate to Korean"
    IMAGE_ANALYSIS = "Image Analysis"

class Subtype(Enum):
    YOUTUBE = "youtube"
    WEBURL = "webpage"
    HTML_TEXT = "html_text"
    MARKDOWN = "markdown"
    LONGTEXT = "longtext"
    IMAGE = "image"


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
        raise TemplateNotFoundError(f'Template file not found: {template_yaml}')

    config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
    templates = config.get('TEMPLATES', {})
    if not isinstance(templates, dict) or not templates:
        raise TemplateFormatError('Template file contains no valid templates')

    print(f"command: {command}, subtype: {subtype}")

    if command == Commands.SUMMARY:
        assert subtype is not None, "subtype is required"
        if subtype == Subtype.YOUTUBE:
            return templates.get('youtube summary', "")
        elif subtype == Subtype.HTML_TEXT or subtype == Subtype.WEBURL:
            return templates.get('webtext summary', "")
    elif command == Commands.QA:
        return templates.get('q&a on context', "")
    # elif command == Commands.META_PROMPT:
    #     return templates.get('meta prompt', "")
    elif command == Commands.IMAGE_ANALYSIS:
        return templates.get('image analysis', "")
    elif command == Commands.TRANSLATE_TO_KOREAN:
        return templates.get('translate to korean', "")

    raise TemplateNotFoundError(f"Template not found for command: {command}, subtype: {subtype}")


def is_url(string: str) -> bool:
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.match(pattern, string) is not None

def get_command(items: list[ClipboardData], auto: bool = False, data_type: str = 'text') -> tuple[Commands, Subtype | None] | None:
    # verify text
    url_text = ''
    long_text = ''
    for item in items:
        if item.type != 'text': continue
        text_data = str(item.data) if isinstance(item.data, str) else ""
        if len(text_data) < 300:
            if not is_url(text_data):
                raise Warning("No valid text:\n"+text_data[:100])
            url_text = text_data
        else:
            long_text = text_data

    if DEBUG: print(f"url_text: {url_text}, long_text: {long_text[:100]} ... {long_text[-100:]}")

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

        if data_type == 'image':
            commands = [cmd.value for cmd in Commands if cmd == Commands.IMAGE_ANALYSIS]
        else:
            commands = [cmd.value for cmd in Commands if cmd != Commands.IMAGE_ANALYSIS]

        rofi = subprocess.run(
            cmd,
            input='\n'.join(commands),
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
    elif command == Commands.SUMMARY or command == Commands.QA or command == Commands.TRANSLATE_TO_KOREAN:

        if url_text:
            if ('youtube.com/watch' in url_text) or ('youtu.be/' in url_text):
                return Commands.SUMMARY, Subtype.YOUTUBE
            return command, Subtype.WEBURL
        else:

            txt_type, stat = get_text_type(long_text)
            print(f"text_type: {txt_type}, status: {stat}")
            if txt_type == "html":
                return command, Subtype.HTML_TEXT
            elif txt_type == "markdown":
                return command, Subtype.MARKDOWN
            elif txt_type == "plain":
                return command, Subtype.LONGTEXT

        raise ContentNotFoundError(f"No valid content found in clipboard data")
    else:
        return command, None

def is_valid_clipboard_data(items:list[ClipboardData]) -> bool:
    for item in items:
        if item.type != 'text': continue
        text_data = str(item.data) if isinstance(item.data, str) else ""
        if len(text_data) < 300:
            if not is_url(text_data):
                return False
    return len(items) > 0

def main(args) -> int:
    command, subtype = None, None
    try:
        Config(args.template)
        #
        # context
        #
        items:list[ClipboardData] = []

        cb_cached = ClipboardCache.get_data()
        if cb_cached:
            items.append(ClipboardData(type="text", data=cb_cached['data']))
            print(f"cached reason: {cb_cached['reason']}")

        clipboard_data:ClipboardData|None = get_clipboard_data()
        if clipboard_data is not None:
            items.append(clipboard_data)
        if DEBUG: print(f"items: len: {len(items)}, {[item.type for item in items]}")
        if not is_valid_clipboard_data(items):
            # get content from active window
            if copy_youtube_url() or copy_html_text():
                items = [get_clipboard_data()] # type:ignore
            else:
                raise Warning("No valid content found in clipboard data")

        cmdinfo = get_command(items, args.auto, items[0].type)
        if cmdinfo is None:
            raise Warning("No command found")

        command, subtype = cmdinfo
        template  = get_template(args.template, command, subtype)
        assert template, "template is empty"
        formatted = ""

        notify_send(command.value, subtype.value if subtype else None)
        if command == Commands.SUMMARY or command == Commands.TRANSLATE_TO_KOREAN:
            assert subtype is not None, "subtype is required"
            if subtype == Subtype.YOUTUBE:
                notify_cont(command.name, "youtube content")
                url = str(items[0].data)
                transcript = str(items[1].data) if len(items) > 1 else ""
                content = youtube.get_youtube_content(url, transcript)

            elif subtype == Subtype.HTML_TEXT:
                notify_cont(command.name, "html text content")
                html_text: str = str(items[0].data) if items[0].type == 'text' else ""
                content = webpage.from_html_text(html_text)

            elif subtype == Subtype.WEBURL:
                notify_cont(command.name, "weburl content")
                url: str = str(items[0].data) if items[0].type == 'text' else ""
                html_text = webpage.get_html(url)
                content = webpage.from_html_text(html_text)

            formatted = template.format( **content )

        elif command == Commands.QA:
            if subtype == Subtype.HTML_TEXT:
                notify_cont("q&a", "html text content")
                html_text: str = str(items[0].data) if items[0].type == 'text' else ""
                content = webpage.from_html_text(html_text)
                context = content.get('content_text', '')
            else:
                assert subtype == Subtype.LONGTEXT
                qa_data = str(items[0].data) if items[0].type == 'text' else ""
                context = q_and_a.get_QandA(qa_data)

            formatted = template.format( context = context, user_query = "user_query here" )

        # elif command == Commands.META_PROMPT:
        #     src_prompt = str(items[0].data) if items[0].type == 'text' else ""
        #     content = meta_prompt.get_prompt(src_prompt)
        #     formatted = template.format( **content )

        elif command == Commands.IMAGE_ANALYSIS:
            content = {'image_data': items}
            formatted = template.format( **content ) # content will beignored

        if DEBUG:
            print(f'Template choice: {command}, {subtype}')
            print(f'Template length: {len(template)} characters')
            print(f'Formatted output length: {len(formatted)} characters')

        #
        # ai processing
        #
        if formatted:
            if Config.use_api:
                notify_cont(command.name, "ai processing...")
                result = openai_inference(formatted, )
                Path("asset/result.md").write_text(result)
                subprocess.run(["mdviewer.app", "asset/result.md"], check=False)
            else:
                # if args.auto:
                run_web_llm(Config.browser_profile, Config.webai, wait_title=Config.webai_title)

                if command == Commands.IMAGE_ANALYSIS:
                    paste() # paste image to chatgpt
                    time.sleep(1.5)

                set_clipboard_data( ClipboardData(type="text", data=formatted) ) # set formatted text to clipboard
                paste(return_key=args.auto) # paste formatted text to chatgpt

                if Config.clear_generated:
                    clear_clipboard()
                # elif command == Commands.IMAGE_ANALYSIS:
                #     set_clipboard_data(clipboard_data) # restore original image

        notify_close()
        ClipboardCache.clear()
        return 0

    except Warning as e:
        notify_send("Warning", str(e), timeout_ms=1000)
        return 1
    except Exception as e:
        if DEBUG:
            print(f"error: {e}")
            import traceback
            traceback.print_exc()

        error_msg = f"{command}, {subtype}: {str(e)}"
        if len(error_msg) > 250:
            error_msg = error_msg[:100]+'\n...\n'+error_msg[-100:]
        subprocess.run(["notify-send", "-u", "critical", type(e).__name__, error_msg], check=False)
        return 1

def test():
    Config("asset/template2.yaml")

    run_web_llm(Config.browser_profile, Config.webai, wait_title=Config.webai_title)
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
        # test()

    sys.exit(main(args))
