from pathlib import Path
from typing import Any

import yaml

import webpage
import youtube
from command import Command
from datatype import Datatype
from exceptions import TemplateFormatError, TemplateNotFoundError
from text_info2 import html_to_md
from ui import error, toast


def transform_data(dtype: Datatype, data: str | Any) -> dict | None:
    """
    Transform raw clipboard data into structured content dictionary.

    This function handles data reformatting for different content types:
    - YouTube URLs: Extract transcript and video metadata
    - Web URLs: Fetch HTML and convert to markdown
    - HTML text: Parse and convert to markdown
    - Markdown/plain text: Normalize formatting
    - Images: Extract blob data and dimensions

    Args:
        dtype: The type of data being processed
        data: Raw clipboard data (URL string, text, or image tuple)

    Returns:
        Structured content dictionary with format-specific fields,
        or None if data type is not supported
    """
    toast(f"{dtype}: processing...")

    match dtype:
        case Datatype.YOUTUBE:
            result = youtube.get_youtube_content(url=str(data))
            return {
                "content_format": "youtube",
                "content_text": result.get("transcript", ""),
                "video_id": result.get("video_id", ""),
            }

        case Datatype.WEBURL:
            text = webpage.get_html_from_url(str(data))
            md_text = html_to_md(text)
            return {"content_format": "markdown", "content_text": md_text.strip()}

        case Datatype.HTML_TEXT:
            text = webpage.from_html_text(str(data))
            md_text = html_to_md(text)
            return {"content_format": "markdown", "content_text": md_text.strip()}

        case Datatype.MARKDOWN:
            return {"content_format": "markdown", "content_text": str(data).strip()}

        case Datatype.LONGTEXT:
            return {"content_format": "text", "content_text": str(data).strip()}

        case Datatype.IMAGE:
            image_data, w, h = data
            return {
                "content_format": "image",
                "blob": image_data,
                "width": w,
                "height": h,
            }

    return None


def get_template(template_path: str, command: Command, dtype: Datatype) -> str:
    template_yaml = Path(template_path).expanduser()
    if not template_yaml.exists():
        raise TemplateNotFoundError(f"Template file not found: {template_yaml}")

    config = yaml.safe_load(template_yaml.read_text(encoding="utf-8")) or {}
    templates = config.get("TEMPLATES", {})
    if not isinstance(templates, dict) or not templates:
        raise TemplateFormatError("Template file contains no valid templates")

    print(f"command: {command}, dtype: {dtype}")

    if command == Command.SUMMARY:
        assert dtype is not None, "dtype is required"
        if dtype == Datatype.YOUTUBE:
            return templates.get("youtube summary", "")
        if dtype == Datatype.HTML_TEXT or dtype == Datatype.WEBURL:
            return templates.get("webtext summary", "")

    elif command == Command.QA:
        return templates.get("q&a on context", "")

    elif command == Command.TRANSLATE_TO_KOREAN:
        if dtype == Datatype.YOUTUBE:
            return templates.get("transcript to korean", "")
        return templates.get("translate to korean", "")
    elif command == Command.TRANSLATE_TO_KOREAN_FILE:
        return templates.get("translate to korean(file)", "")

    elif command == Command.IMAGE_ANALYSIS:
        return templates.get("image analysis", "")

    raise TemplateNotFoundError(
        f"Template not found for command: {command}, dtype: {dtype}"
    )


def format_with_template(
    template_path: str, command: Command, dtype: Datatype, content: dict
) -> dict:
    """
    Load template from YAML file and format it with content data.

    This function retrieves the appropriate template based on command and data type,
    then formats it using the provided content dictionary.

    Args:
        template_path: Path to YAML template file (e.g., "asset/template2.yaml")
        command: The command type (SUMMARY, QA, TRANSLATE_TO_KOREAN, etc.)
        dtype: The data type (YOUTUBE, WEBURL, HTML_TEXT, etc.)
        content: Structured content dictionary from transform_data()

    Returns:
        Content dictionary with added "template" field containing formatted prompt text

    Raises:
        TemplateNotFoundError: If template file or specific template not found
        TemplateFormatError: If template file format is invalid
    """
    template = get_template(template_path, command, dtype)

    if content is not None:
        content["template"] = template.format(**content)
    return content


def get_prompt(
    template_path: str, command: Command, dtype: Datatype, data: str | Any
) -> dict:
    """
    Generate formatted prompt by transforming data and applying template.

    This is the main orchestrator function that combines data transformation
    and template formatting into a single operation.

    Args:
        template_path: Path to YAML template file
        command: The command type determining template selection
        dtype: The data type determining transformation logic
        data: Raw clipboard data to transform

    Returns:
        Dictionary containing transformed content and formatted template

    Raises:
        TemplateNotFoundError: If template cannot be found
        TemplateFormatError: If template format is invalid
    """
    content: dict = transform_data(dtype, data)
    return format_with_template(template_path, command, dtype, content)


if __name__ == "__main__":
    # youtube transcript download test
    try:
        test = youtube.get_youtube_content(
            url="https://www.youtube.com/watch?v=ty9uyJEY4EQ"
        )
        print(test)
    except Exception as ex:
        error(str(ex))

    # command = Command.SUMMARY
    # dtype = Datatype.YOUTUBE
    # data = "https://www.youtube.com/watch?v=oN9uQ84VnqE"
    # prompt = get_prompt("asset/template2.yaml", command, dtype, data)
    # print(prompt)
