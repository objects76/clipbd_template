
import requests
import time
import os


def get_html(url):
    import requests
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme in ['http', 'https']:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    elif parsed.scheme == 'file':
        with open(parsed.path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"지원하지 않는 URL 스키마: {parsed.scheme}")

from firecrawl_to_md import firecrawl_to_md
from jina_to_md import jina_to_md

def crawling(url):
    if not url.startswith('https:') and not url.startswith('http:'):
        raise ValueError("Invalid URL")

    try:
        return 'Markdown', jina_to_md(url)
    except Exception as e:
        pass

    try:
        return 'Markdown', firecrawl_to_md(url)
    except Exception as e:
        pass

    return 'HTML', get_html(url)


if __name__ == "__main__":
    # print( crawling("https://news.hada.io/topic?id=22490") )
    print( crawling("https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram") )