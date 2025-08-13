#!/usr/bin/env python3
"""
Script to find matching </article> tag for <article class="meteredContent">
and export the complete article section to content.html
"""

import requests
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import sys

ALLOWED_TAGS = {
    "article", "section",
    "h1", "h2", "h3", "h4",
    "p", "pre", "code", "ul", "ol", "li",
    "blockquote",
    "figure", "figcaption",
    "a",
}


def _remove_scripts_styles_comments(root):
    for el in root(["script", "style"]):
        el.decompose()
    for c in root.find_all(string=lambda x: isinstance(x, Comment)):
        c.extract()


def _unwrap_disallowed_tags(root):
    for tag in list(root.find_all(True)):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()


def _strip_attributes(root):
    for tag in root.find_all(True):
        if tag.name == "a":
            href = tag.get("href")
            tag.attrs = {}
            if href:
                tag.attrs["href"] = href
        else:
            tag.attrs = {}  # drop all attrs on allowed structural tags


def _drop_empty_tags(root):
    def is_empty(t):
        # Keep <pre>, <code>, <blockquote> even if short/whitespace
        if t.name in ("pre", "code", "blockquote"):
            return False
        # no text and no children
        text = (t.get_text(strip=True) or "")
        return len(text) == 0 and len(list(t.children)) == 0

    for tag in list(root.find_all(True)):
        if is_empty(tag):
            tag.decompose()

def compress_medium(html: str):
    """Return (cleaned_html, plain_text)."""
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("article") or soup  # preserve article boundary if present
    _remove_scripts_styles_comments(root)
    _unwrap_disallowed_tags(root)
    _strip_attributes(root)
    _drop_empty_tags(root)
    cleaned_html = str(root)
    return cleaned_html

def extract_medium(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    article = soup.find('article', attrs={'class': 'meteredContent'})

    if article:
        return "```html\n" + compress_medium(str(article)) + "\n```"
    raise ValueError("No article found")


if __name__ == '__main__':
    with open('temp/input.html', 'rt') as fp:
        html_content = fp.read()

    extracted = extract_medium(html_content)
    print(extracted)
    with open('temp/output.html', 'wt') as fp:
        fp.write(extracted)

