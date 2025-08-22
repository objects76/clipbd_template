#!/usr/bin/env python3
import subprocess
import pyperclip
from pathlib import Path
import sys
import yaml
import clipbd
import time
from clipbd import get_lastest_clipboard

VERSION = "1.0.0"

DEBUG = True


def llm(user: str, url: str) -> None:
    BROWSER = "microsoft-edge-stable"
    subprocess.run([
        BROWSER,
        f"--profile-directory={user}",
        "--new-tab",
        url
    ])

def resource_path(name: str) -> Path:
    ''' get file path from packed executable '''
    try:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base / name
    except Exception as ex:
        print(ex)
        return Path(name)

def get_template(template_path, choice = None):
    template_yaml = Path(template_path).expanduser()
    if not template_yaml.exists():
        raise ValueError(f'not found: {template_yaml}')

    config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
    templates = config.get('TEMPLATES', {})
    if not isinstance(templates, dict) or not templates:
        raise ValueError('no templates')

    if choice is None:
        # ~/.config/rofi/
        cmd = [
            'rofi', '-dmenu', '-no-custom',
            # '-monitor', '-3',
            '-theme-str', 'window {width: 10%;} entry { enabled: false; }',
            '-p', f'Choose {VERSION}:',
            '-dpi', '192',
            '-lines', f'{len(templates)}',
            '-no-fixed-num-lines',
        ]

        rofi = subprocess.run(
            cmd,
            input='\n'.join(templates.keys()),
            text=True,
            capture_output=True,
        )

        choice = (rofi.stdout or '').strip()
        if not choice or choice not in templates:
            return "", ""
    return choice, templates[choice]


def auto_selector():
    items = get_lastest_clipboard(n=1, include_images=False)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()

    text = text or ''
    if 'youtube.com/watch' in text or 'youtu.be/' in text:
        return 'youtube summary'
    elif text.startswith('https://') or text.startswith('http://'):
        return 'webpage summary'
    elif text.count('.medium.com') > 10:
        return 'webpage summary'
        # return 'medium summary'
    elif len(text) > 500:
        return 'webpage summary'

    return "invalid"

def manual_selector():
    pass

from medium import MediumError
def webpage_summary():
    try:
        return clipbd.get_medium()
    except MediumError as e:
        print(e)
        pass

    try:
        return clipbd.get_webpage()
    except Exception as e:
        print(e)
        pass

    return clipbd.get_longtext()

def main(args) -> int:

    choice = auto_selector() if args.auto else None
    choice, template  = get_template(args.template, choice)

    try:
        formatted = ""
        if choice == 'youtube summary':
            formatted = template.format( **clipbd.get_youtube_content() )
        # elif choice == 'medium summary':
        #     formatted = template.format( **clipbd.get_medium() )
        elif choice == 'webpage summary':
            formatted = template.format( **webpage_summary() )
        elif choice == 'meta prompt':
            formatted = template.format( **clipbd.get_prompt() )
        elif choice == 'q&a on context':
            formatted = template.format( **clipbd.get_QandA() )

        if DEBUG: print(f'{choice=}')
        if DEBUG: print(f'{template=}')
        if DEBUG: print(f'{formatted=}')

        if formatted:
            if args.auto:
                llm("Default", "https://www.chatgpt.com")
                time.sleep(1)

            pyperclip.copy(formatted)
            time.sleep(0.3)
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v', 'Return'])
            # time.sleep(0.5)
            # subprocess.run(['xdotool', 'key', 'Return'])
            # clipbd.clear_lastest_clipboard(n=1)

        return 0
    except Exception as e:
        subprocess.run(["notify-send", "-u", "critical", "error", f"{choice}: {str(e)}"], check=False)
        return 1


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', '-t', help='Template file path', default='~/.config/rofi/template.yaml')
    parser.add_argument('--auto', '-a', help='Auto select template', action='store_true')
    parser.add_argument('--test', '-x', help='Test script', action='store_true')
    args = parser.parse_args()

    if args.test:
        import time
        for i in range(5):
            print(f"{i+1}초 대기 중...")
            time.sleep(1)

    sys.exit(main(args))
