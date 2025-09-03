import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from exceptions import WebExtractionError
from text_info2 import html_to_md




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
        raise WebExtractionError(f"Unsupported URL scheme: {parsed.scheme}")


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
    # html to md test
    from pathlib import Path
    html_text = Path("asset/docs.html").read_text(encoding='utf-8')
    md_text = html_to_md(html_text)
    Path("asset/docs.md").write_text(html_to_md(html_text))

