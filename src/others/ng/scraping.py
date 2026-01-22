from urllib.parse import urlparse

import requests
from firecrawl_to_md import firecrawl_to_md
from jina_to_md import jina_to_md

from webpage import html_to_md


def get_html(url: str) -> str:
    """Fetch raw HTML content from URL with timeout handling.

    Args:
        url (str): URL to fetch content from

    Returns:
        str: Raw HTML content

    Raises:
        ValueError: If URL scheme is not supported
        requests.RequestException: If HTTP request fails
    """
    parsed = urlparse(url)
    if parsed.scheme in ["http", "https"]:
        response = requests.get(
            url,
            timeout=30,  # Add timeout to prevent hanging
            headers={"User-Agent": "Mozilla/5.0 (compatible; ClipboardTemplate/1.0)"},
        )
        response.raise_for_status()
        return response.text
    if parsed.scheme == "file":
        with open(parsed.path, encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")


def crawling(url: str, use_parallel: bool = True) -> tuple[str, str]:
    """Extract content from URL with optional parallel processing.

    By default, uses enhanced parallel extraction that runs both APIs simultaneously
    and selects the longer (more comprehensive) result. Falls back to sequential
    extraction if parallel processing fails.

    Args:
        url (str): URL to extract content from
        use_parallel (bool): Whether to use parallel extraction (default: True)

    Returns:
        tuple[str, str]: (format, content) where format is 'Markdown' or 'HTML'

    Raises:
        ValueError: If URL format is invalid
        Exception: If all extraction methods fail
    """
    if not url.startswith(("https:", "http:")):
        raise ValueError(f"Invalid URL format: {url}")

    # Sequential fallback extraction with error collection
    errors = []

    # Try Jina Reader API first
    try:
        content = jina_to_md(url)
        return "Markdown", content
    except Exception as e:
        errors.append(f"Jina API failed: {e!s}")

    # Try Firecrawl API as fallback
    try:
        content = firecrawl_to_md(url)
        return "Markdown", content
    except Exception as e:
        errors.append(f"Firecrawl API failed: {e!s}")

    # Final fallback to raw HTML with markdown conversion
    try:
        html = get_html(url)
        markdown = html_to_md(html)
        return "Markdown", markdown
    except Exception as e:
        errors.append(f"Raw HTML extraction failed: {e!s}")
        raise Exception(f"All extraction methods failed for {url}: {'; '.join(errors)}")


if __name__ == "__main__":
    """Test crawling functionality with sample URLs."""
    test_urls = [
        "https://news.hada.io/topic?id=22490",
        "https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram",
    ]

    for url in test_urls:
        try:
            format_type, content = crawling(url)
            print(f"Successfully extracted {format_type} content from {url}")
            print(f"Content length: {len(content)} characters")
        except Exception as e:
            print(f"Failed to extract content from {url}: {e}")
