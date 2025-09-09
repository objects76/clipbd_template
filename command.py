
import subprocess
from enum import Enum
from datatype import Datatype
from typing import Any
from text_info2 import html_to_md
class Command(Enum):
    SUMMARY = "Summary"
    QA = "Q&A"
    TRANSLATE_TO_KOREAN = "Translate to Korean"
    IMAGE_ANALYSIS = "Image Analysis"


def get_dmenu(choices:list[Command], initial_selection:int = 0) -> str:
    cmd = [
        'rofi', '-dmenu', # '-no-custom',
        '-theme-str', 'window {width: 10%;} listview {scrollbar: false;} inputbar {enabled: false;}',
        '-lines', str(len(choices)),
        '-no-fixed-num-lines',
        '-hover-select', '-me-select-entry', '', '-me-accept-entry', 'MousePrimary',
        '-kb-accept-entry', "Return,space",
        '-selected-row', str(initial_selection),  # Set initial selection to first item (0-indexed)
    ]
    rofi = subprocess.run(
            cmd,
            input='\n'.join([c.value for c in choices]),
            text=True,
            capture_output=True,
            timeout=30  # Prevent hanging
        )
    return (rofi.stdout or '').strip()




def get_command(dtype: Datatype, data:str|Any) -> Command | None:
    choices:list[Command] = []
    match dtype:
        case Datatype.YOUTUBE | Datatype.WEBURL | Datatype.HTML_TEXT | Datatype.MARKDOWN:
            choices.extend([Command.SUMMARY, Command.QA])
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


import youtube
import webpage

def post_process(dtype: Datatype, data:str|Any) -> str|dict|tuple[bytes, int, int] | None:
    match dtype:
        case Datatype.YOUTUBE:
            return youtube.get_youtube_content(str(data), "")

        case Datatype.WEBURL:
            text = webpage.get_html_from_url(str(data))
            md_text = html_to_md(text)
            return {"content_format" : "markdown", "content_text" : md_text}

        case Datatype.HTML_TEXT:
            text = webpage.from_html_text(str(data))
            md_text = html_to_md(text)
            return {"content_format" : "markdown", "content_text" : md_text}

        case Datatype.MARKDOWN:
            return {"content_format" : "markdown", "content_text" : str(data)}

        case Datatype.LONGTEXT:
            return {"content_format" : "text", "content_text" : str(data)}

        case Datatype.IMAGE:
            image_data, w, h = data
            return {"content_format" : "image", "blob" : image_data, "width" : w, "height" : h}

    return None



def get_template(template_path: str, command: Command, dtype: Datatype) -> str:
    template_yaml = Path(template_path).expanduser()
    if not template_yaml.exists():
        raise TemplateNotFoundError(f'Template file not found: {template_yaml}')

    config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
    templates = config.get('TEMPLATES', {})
    if not isinstance(templates, dict) or not templates:
        raise TemplateFormatError('Template file contains no valid templates')

    print(f"command: {command}, dtype: {dtype}")

    if command == Commands.SUMMARY:
        assert dtype is not None, "dtype is required"
        if dtype == Subtype.YOUTUBE:
            return templates.get('youtube summary', "")
        elif dtype == Subtype.HTML_TEXT or dtype == Subtype.WEBURL:
            return templates.get('webtext summary', "")

    elif command == Commands.QA:
        return templates.get('q&a on context', "")

    elif command == Commands.TRANSLATE_TO_KOREAN:
        if dtype == Datatype.YOUTUBE:
            return templates.get('transcript to korean', "")
        else:
            return templates.get('translate to korean', "")

    elif command == Commands.IMAGE_ANALYSIS:
        return templates.get('image analysis', "")

    raise TemplateNotFoundError(f"Template not found for command: {command}, dtype: {dtype}")



def main():
    import subprocess
    from datatype import get_clipboard
    template_path = 'asset/template2.yaml'

    cb_data = get_clipboard()
    if cb_data is None:
        print("No clipboard data")
        return

    dtype, data = cb_data
    subprocess.run(["notify-send", "-u", "normal", str(dtype), 'processing...'], check=False)
    data = post_process(dtype, data)

    command = get_command(dtype, data)
    print(command)
    print(data)
    return

    processed_data = post_process(dtype, data)
    print('======================', dtype, type(processed_data).__name__, '======================')
    for k,v in processed_data.items():
        if len(v) > 250:
            print(f"{k}: {len(v)}, ", v[:100] + "\n...\n" + v[-100:] )
        else:
            print(f"{k}: {len(v)}, ", v)
    # command = get_command(dtype, data)
    # print(command)


if __name__ == "__main__": main()

