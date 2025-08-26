import re
THRESHOLD = 70

def html_hit_count(text: str) -> int:
    patterns = [
        # r"<!DOCTYPE html>",
        # r"<html.*?>",
        # r"<head.*?>",
        # r"<body.*?>",
        # r"<[a-z]+[^>]*>.*?</[a-z]+>",  # general tag pair
        r"<[a-z]+[^>]*>.*?<\/[a-z]+>",
        # r"<img\s+[^>]*>",              # img tag
        # r"<a\s+href=[\"'][^\"']+[\"']" # links
    ]
    return sum(len(re.findall(p, text, re.MULTILINE)) for p in patterns)


def markdown_hit_count(text: str) -> int:
    patterns = [
        r"^#{1,6}\s",              # headings
        # r"\*{1,2}[^*]+\*{1,2}",    # bold/italic
        # r"\[[^\]]+\]\([^)]+\)",    # links
        r"^\s*[-*+]\s+",           # unordered list
        r"^\s*\d+\.\s+",           # ordered list
        r"`[^`]+`",                # inline code
        r"\|.+\|.+\|"              # tables
    ]
    return sum(len(re.findall(p, text, re.MULTILINE)) for p in patterns)

def is_html(text: str) -> bool:
    return html_hit_count(text) > THRESHOLD

def is_markdown(text: str) -> bool:
    return markdown_hit_count(text) > THRESHOLD


def get_text_type(text: str) -> tuple[str, dict]:
    html_hits = html_hit_count(text)
    md_hits = markdown_hit_count(text)

    info = {"length": len(text), "html_hits": html_hits, "markdown_hits": md_hits}
    if html_hits > md_hits and html_hits > THRESHOLD:
        return "html", info
    elif md_hits > THRESHOLD:
        return "markdown", info
    else:
        return "plain", info


if __name__ == "__main__":
    import pyperclip
    from pathlib import Path

    text = Path('asset/input.html').read_text(encoding='utf-8')
    # text = Path('asset/test.md').read_text(encoding='utf-8')
    # text = Path('asset/text.txt').read_text(encoding='utf-8')
    # text = pyperclip.paste()
    print(get_text_type(text))
    print('length:', len(text))

