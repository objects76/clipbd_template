

from ck_clipboard import ClipboardData
from exceptions import ContentNotFoundError

def get_prompt(text:str):
    items = [ClipboardData(type="text", data=text)]
    for i, item in enumerate(items, start=1):
        if item.type != 'text': continue
        text = str(item.data).strip() if isinstance(item.data, str) else ""
        if len(text) > 10:
            return { "source_prompt": text }

    raise ContentNotFoundError("No valid clipboard data for meta prompt processing")

