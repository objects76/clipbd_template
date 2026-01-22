import re
from html.parser import HTMLParser
from typing import Literal

import html_to_markdown

from exceptions import WebExtractionError

Label = Literal["html", "markdown", "plain"]


class HtmlCounter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.start_tags = 0
        self.end_tags = 0
        self.self_closing = 0
        self.attrs_total = 0
        self.errors = 0

    def handle_starttag(self, tag, attrs):
        self.start_tags += 1
        self.attrs_total += len(attrs)

    def handle_startendtag(self, tag, attrs):
        self.self_closing += 1
        self.attrs_total += len(attrs)

    def handle_endtag(self, tag):
        self.end_tags += 1

    def error(self, message):
        # html.parser doesn’t raise by default; we just track anomalies
        self.errors += 1


MD_PATTERNS = {
    # counts of very typical Markdown constructs
    "atx_h": re.compile(r"^(#{1,6})\s+\S", re.MULTILINE),
    "fence": re.compile(r"^```.+?^```", re.MULTILINE | re.DOTALL),
    "inline_code": re.compile(r"(?<!`)`[^`\n]+`(?!`)"),
    "links": re.compile(r"\[[^\]]+\]\([^)]+\)"),
    "images": re.compile(r"!\[[^\]]*\]\([^)]+\)"),
    "olist": re.compile(r"(?m)^(?:\d{1,3})\.\s+\S"),
    "ulist": re.compile(r"(?m)^(?:-|\*)\s+\S"),
    "blockquote": re.compile(r"(?m)^>\s+\S"),
}

HTML_STRONG_HINTS = [
    re.compile(r"<!DOCTYPE\s+html", re.IGNORECASE),
    re.compile(r"<html\b", re.IGNORECASE),
    re.compile(
        r"<(head|body|div|span|p|a|ul|ol|li|h[1-6]|table|img|br|hr)\b", re.IGNORECASE
    ),
]

VOID_TAGS = {
    "br",
    "hr",
    "img",
    "input",
    "meta",
    "link",
    "source",
    "track",
    "area",
    "col",
    "embed",
    "wbr",
}


def html_score(text: str) -> float:
    # quick strong hints first
    if any(p.search(text) for p in HTML_STRONG_HINTS):
        base = 2.0
    else:
        base = 0.0

    # structural parse count
    parser = HtmlCounter()
    try:
        parser.feed(text)
    except Exception:
        pass  # keep heuristic robust

    tag_like = len(re.findall(r"</?\w+[^>]*>", text))
    real_tags = parser.start_tags + parser.end_tags + parser.self_closing

    # reward actual parsed tags vs raw angle brackets
    structural = 0.0
    if real_tags:
        structural += 1.0
        # attributes often indicate real HTML
        if parser.attrs_total >= 2:
            structural += 0.5
        # closing tags / balance
        if parser.end_tags or parser.self_closing:
            structural += 0.25

    # small bonus if many void tags appear (common in HTML, rare in MD)
    void_hits = sum(
        len(re.findall(rf"<{t}\b", text, flags=re.IGNORECASE)) for t in VOID_TAGS
    )
    structural += min(void_hits * 0.1, 0.5)

    # penalize if there are lots of angle-bracket-ish things but parser found few real tags
    if tag_like >= 5 and real_tags == 0:
        structural -= 0.5

    return base + structural


def markdown_score(text: str) -> float:
    score = 0.0
    for name, rx in MD_PATTERNS.items():
        hits = len(rx.findall(text))
        if hits:
            # give heavier weight to fenced blocks / headings / links
            weight = {
                "fence": 0.8,
                "atx_h": 0.6,
                "links": 0.5,
                "images": 0.5,
                "olist": 0.4,
                "ulist": 0.4,
                "blockquote": 0.3,
                "inline_code": 0.2,
            }[name]
            score += min(hits, 6) * weight  # cap influence
    return score


def get_text_type(text: str):
    hs = html_score(text)
    ms = markdown_score(text)

    # Handle “Markdown allows raw HTML”: if both are strong, call it mixed
    if hs >= 2.0 and ms >= 1.0:
        label: Label = "html"
        why = "Strong HTML structure detected and multiple Markdown constructs present (Markdown permits raw HTML)."
    elif hs >= 1.5 and hs >= ms + 0.5:
        label = "html"
        why = "HTML-like structure and tags parsed successfully outweigh Markdown cues."
    elif ms >= 1.5 and ms >= hs + 0.5:
        label = "markdown"
        why = "Multiple Markdown-specific constructs dominate over HTML structure."
    else:
        label = "plain"
        why = "Signals are weak or conflicting."

    return label, {
        "html_score": round(hs, 2),
        "markdown_score": round(ms, 2),
        "reason": why,
    }


def compress_html(html: str) -> str:
    """Compress HTML by removing SVG elements to reduce size.

    Args:
        html (str): Original HTML content

    Returns:
        str: Compressed HTML with SVG elements removed
    """

    # Remove entire SVG elements including content
    svg_pattern = r"<svg[^>]*>.*?</svg>"
    compressed = re.sub(svg_pattern, "", html, flags=re.DOTALL | re.IGNORECASE)

    # remove fixed text
    for useless_text in [
        "Press enter or click to view image in full size",
    ]:
        compressed = compressed.replace(useless_text, "")

    return compressed


def compress_md(md: str) -> str:
    """Compress markdown by removing or truncating long SVG images.

    Args:
        md (str): Original markdown content

    Returns:
        str: Compressed markdown with SVG images trimmed
    """

    # Pattern to match SVG images with base64 data
    svg_pattern = r"!\[([^\]]*)\]\(data:image/svg\+xml;base64,[A-Za-z0-9+/=]+\)"

    def replace_svg(match):
        alt_text = match.group(1) or "SVG Image"
        return f"[{alt_text}]"

    # Replace all SVG images with just their alt text
    compressed = re.sub(svg_pattern, replace_svg, md)

    return compressed


def html_to_md(html_text: str) -> str:
    try:
        html_text = compress_html(html_text)
        markdown = html_to_markdown.convert_to_markdown(
            html_text,
            escape_misc=False,
            escape_underscores=False,
            extract_metadata=False,
        )
        # Compress SVG images to reduce size
        compressed_markdown = compress_md(markdown)
        print(
            f"# html to markdown: {len(html_text)} -> {len(markdown)} -> {len(compressed_markdown)} (compressed)"
        )
        return compressed_markdown
    except Exception as e:
        raise WebExtractionError(f"HTML to markdown conversion failed: {e!s}") from e


def str_to_markdown(text: str) -> str:
    textinfo = get_text_type(text)
    if textinfo[0] == "html":
        return html_to_md(text)
    return text


if __name__ == "__main__":
    from pathlib import Path

    text = Path("asset/docs.html").read_text(encoding="utf-8")
    print(str_to_markdown(text))
    print("length:", len(text))
