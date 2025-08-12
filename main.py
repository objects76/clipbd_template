#!/usr/bin/env python3
import subprocess
import pyperclip
from pathlib import Path
import sys
import yaml
import clipbd

DEBUG = True

def resource_path(name: str) -> Path:
    ''' get file path from packed executable '''
    try:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base / name
    except Exception as ex:
        print(ex)
        return Path(name)

def get_template(template_path):
    template_yaml = Path(template_path).expanduser()
    if not template_yaml.exists():
        raise ValueError(f'not found: {template_yaml}')

    config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
    templates = config.get('TEMPLATES', {})
    if not isinstance(templates, dict) or not templates:
        raise ValueError('no templates')

    # ~/.config/rofi/
    cmd = [
        'rofi', '-dmenu', '-no-custom',
        '-monitor', '-3',
        '-theme-str', 'window {width: 10%;} entry { enabled: false; }',
        '-p', 'Choose template:',
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

def main(args) -> int:

    try:
        formatted = ""
        choice, template  = get_template(args.template)
        if choice == 'youtube summary':
            formatted = template.format( **clipbd.get_youtube_content() )
        elif choice == 'article summary':
            formatted = template.format( **clipbd.get_html() )
        elif choice == 'meta prompt':
            formatted = template.format( **clipbd.get_prompt() )
        elif choice == 'q&a on context':
            formatted = template.format( **clipbd.get_QandA() )

        if DEBUG: print(f'{choice=}')
        if DEBUG: print(f'{template=}')
        if DEBUG: print(f'{formatted=}')

        if formatted:

            pyperclip.copy(formatted)
            subprocess.run(['bash', '-c', 'sleep 0.3; xdotool key --clearmodifiers ctrl+v'])
            # clipbd.clear_lastest_clipboard(n=1)

        return 0
    except Exception as e:
        print('exception:', e)
        return 1


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', '-t', help='Template file path', default='~/.config/rofi/template.yaml')
    args = parser.parse_args()
    sys.exit(main(args))
