
import youtube
import webpage
from exceptions import TemplateNotFoundError, TemplateFormatError, ContentNotFoundError
from datatype import Datatype
from typing import Any
from pathlib import Path
import yaml
from command import Command
import subprocess
from text_info2 import html_to_md

def post_process(dtype: Datatype, data:str|Any) -> str|dict|tuple[bytes, int, int] | None:

    subprocess.run(["notify-send", "-u", "normal", str(dtype), 'processing...'], check=False)

    match dtype:
        case Datatype.YOUTUBE:
            return youtube.get_youtube_content(str(data), "")

        case Datatype.WEBURL:
            text = webpage.get_html_from_url(str(data))
            md_text = html_to_md(text)
            return {"content_format" : "markdown", "content_text" : md_text.strip()}

        case Datatype.HTML_TEXT:
            text = webpage.from_html_text(str(data))
            md_text = html_to_md(text)
            return {"content_format" : "markdown", "content_text" : md_text.strip()}

        case Datatype.MARKDOWN:
            return {"content_format" : "markdown", "content_text" : str(data).strip()}

        case Datatype.LONGTEXT:
            return {"content_format" : "text", "content_text" : str(data).strip()}

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

    if command == Command.SUMMARY:
        assert dtype is not None, "dtype is required"
        if dtype == Datatype.YOUTUBE:
            return templates.get('youtube summary', "")
        elif dtype == Datatype.HTML_TEXT or dtype == Datatype.WEBURL:
            return templates.get('webtext summary', "")

    elif command == Command.QA:
        return templates.get('q&a on context', "")

    elif command == Command.TRANSLATE_TO_KOREAN:
        if dtype == Datatype.YOUTUBE:
            return templates.get('transcript to korean', "")
        else:
            return templates.get('translate to korean', "")
    elif command == Command.TRANSLATE_TO_KOREAN_FILE:
        return templates.get('translate to korean(file)', "")

    elif command == Command.IMAGE_ANALYSIS:
        return templates.get('image analysis', "")

    raise TemplateNotFoundError(f"Template not found for command: {command}, dtype: {dtype}")


def get_prompt(template_path: str, command: Command, dtype: Datatype, data:str|Any) -> str:
    template = get_template(template_path, command, dtype)

    content = post_process(dtype, data)

    print(f"content: {content.keys()}")
    return template.format( **content )


if __name__ == "__main__":
    command = Command.SUMMARY
    dtype = Datatype.YOUTUBE
    data = "https://www.youtube.com/watch?v=oN9uQ84VnqE"
    prompt = get_prompt('asset/template2.yaml', command, dtype, data)
    print(prompt)

