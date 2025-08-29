import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import html_to_markdown
import requests


def compress_html(html: str) -> str:
    """Compress HTML by removing SVG elements to reduce size.

    Args:
        html (str): Original HTML content

    Returns:
        str: Compressed HTML with SVG elements removed
    """

    # Remove entire SVG elements including content
    svg_pattern = r'<svg[^>]*>.*?</svg>'
    compressed = re.sub(svg_pattern, '', html, flags=re.DOTALL | re.IGNORECASE)

    # remove fixed text
    for useless_text in [
        "Press enter or click to view image in full size",
    ]:
        compressed = compressed.replace(useless_text, '')

    return compressed



def compress_md(md: str) -> str:
    """Compress markdown by removing or truncating long SVG images.

    Args:
        md (str): Original markdown content

    Returns:
        str: Compressed markdown with SVG images trimmed
    """

    # Pattern to match SVG images with base64 data
    svg_pattern = r'!\[([^\]]*)\]\(data:image/svg\+xml;base64,[A-Za-z0-9+/=]+\)'

    def replace_svg(match):
        alt_text = match.group(1) or "SVG Image"
        return f"[{alt_text}]"

    # Replace all SVG images with just their alt text
    compressed = re.sub(svg_pattern, replace_svg, md)

    return compressed

def html_to_md(html: str) -> str:
    try:
        html = compress_html(html)
        markdown = html_to_markdown.convert_to_markdown(
            html,
            escape_misc = False,
            escape_underscores = False,
            extract_metadata = False,
            )
        # Compress SVG images to reduce size
        compressed_markdown = compress_md(markdown)
        print(f"# html to markdown: {len(html)} -> {len(markdown)} -> {len(compressed_markdown)} (compressed)")
        return compressed_markdown
    except Exception as e:
        raise Exception(f"html to markdown: {str(e)}")



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
    if parsed.scheme in ['http', 'https']:
        response = requests.get(
            url,
            timeout=30,  # Add timeout to prevent hanging
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; ClipboardTemplate/1.0)'
            }
        )
        response.raise_for_status()
        return response.text
    elif parsed.scheme == 'file':
        with open(parsed.path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")


def from_html_text(html_text: str):
    result = { "source_url": "Not provided" }

    # medium filtering
    soup = BeautifulSoup(html_text, "html.parser")
    node = soup.find('article', attrs={'class': 'meteredContent'})
    node = node or soup.find('section')
    node = node or soup

    result["content_format"] = "markdown"
    result["content_text"] = html_to_md( str(node) )


    return result

if __name__ == "__main__":
    with open("asset/input.html", "r") as f:
        html = f.read()
    print(html_to_md(html))
