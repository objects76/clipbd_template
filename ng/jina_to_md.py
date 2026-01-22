import os

import requests
from dotenv import load_dotenv

from dunstify import notify_cont

load_dotenv(os.path.expanduser("~/.config/rofi/.env"))
jjkim_key = os.getenv("JINA_API_JJKIM")
obj76_key = os.getenv("JINA_API_OBJECTS76")

# Jina Reader API integration
# Documentation: https://jina.ai/reader/
API_CALL_TIMEOUT = 120

instruction = (
    "Extract the main content from the given HTML and convert it to Markdown format."
)


def jina_to_md(target_url: str) -> str:
    """Extract content from URL using Jina Reader API.

    Args:
        target_url (str): URL to extract content from

    Returns:
        str: Markdown formatted content

    Raises:
        Exception: If all API keys fail or no keys available
    """
    notify_cont("jina to markdown", f"jina({target_url}) to markdown")
    request_url = f"https://r.jina.ai/{target_url}"

    api_keys = [key for key in [jjkim_key, obj76_key] if key]
    if not api_keys:
        raise Exception("No Jina API keys found in environment variables")

    last_exception = None

    for key in api_keys:
        try:
            response = requests.get(
                request_url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "X-Respond-With": "readerlm-v2",
                },
                timeout=API_CALL_TIMEOUT,  # Add timeout to prevent hanging
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text
        except Exception as e:
            last_exception = e
            continue

    raise Exception(f"All Jina API keys failed for {target_url}: {last_exception!s}")


def test():
    """Test Jina API with a sample URL."""
    try:
        md_text = jina_to_md("https://huggingface.co/jinaai/ReaderLM-v2")
        print(md_text)
    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    test()
