
import subprocess
from enum import Enum
from datatype import Datatype
from typing import Any
from text_info2 import html_to_md

class Command(Enum):
    SUMMARY = "Summary"
    QA = "Q&A"
    TRANSLATE_TO_KOREAN = "Translate to Korean"
    TRANSLATE_TO_KOREAN_FILE = "Translate to Korean(File)"
    IMAGE_ANALYSIS = "Image Analysis"


def get_dmenu(choices:list[Command], initial_selection:int = 0, timeout_sec: int = 30) -> str:
    cmd = [
        'rofi', '-dmenu', # '-no-custom',
        '-theme-str', 'window {width: 10%;} listview {scrollbar: false;} inputbar {enabled: false;}',
        '-lines', str(len(choices)),
        '-no-fixed-num-lines',
        '-hover-select', '-me-select-entry', '', '-me-accept-entry', 'MousePrimary',
        '-kb-accept-entry', "Return,space",
        '-auto-select', '-selected-row', str(initial_selection),
    ]
    try:
        rofi = subprocess.run(
            cmd,
            input='\n'.join([c.value for c in choices]),
            text=True,
            capture_output=True,
            timeout=timeout_sec,  # automatically stop waiting after timeout_sec
        )
        return (rofi.stdout or '').strip()
    except subprocess.TimeoutExpired:
        return ''
        return choices[initial_selection].value

def get_command(dtype: Datatype, data:str|Any) -> Command | None:
    choices:list[Command] = []
    match dtype:
        case Datatype.YOUTUBE | Datatype.WEBURL | Datatype.HTML_TEXT | Datatype.MARKDOWN:
            choices.extend([Command.SUMMARY, Command.QA, Command.TRANSLATE_TO_KOREAN])
        case Datatype.LONGTEXT:
            choices.extend([Command.SUMMARY, Command.QA, Command.TRANSLATE_TO_KOREAN])
        case Datatype.IMAGE:
            choices.extend([Command.IMAGE_ANALYSIS])

    if not choices:
        return None

    choice = get_dmenu(choices, 0)
    if not choice:
        return None
    return Command(choice)



def main():
    import subprocess
    from datatype import get_clipboard
    template_path = 'asset/template2.yaml'

    cb_data = get_clipboard()
    if cb_data is None:
        print("No clipboard data")
        return

    dtype, data = cb_data
    command = get_command(dtype, data)
    print(command)
    print(data)
    return



if __name__ == "__main__": main()

