import os
import time

from dotenv import load_dotenv

load_dotenv()

# 🔑 API Keys (Replace with your actual keys)
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
# FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
# # 🔗 API URLs
# FIRECRAWL_START_URL = FIRECRAWL_BASE_URL
# FIRECRAWL_STATUS_URL = "https://api.firecrawl.ai/status"
# FIRECRAWL_RESULTS_URL = "https://api.firecrawl.ai/results"
#
# # Step 1: Start Firecrawl AI-powered web scraping
# firecrawl_payload = {
#     "domain": "https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide",
#     # "keywords": ["AI", "Machine Learning"],
#     "max_pages": 5
# }
#
# firecrawl_response = requests.post(
#     FIRECRAWL_START_URL,
#     json=firecrawl_payload,
#     headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
# )
# firecrawl_data = firecrawl_response.json()
#
# # Extract Crawl ID
# crawl_id = firecrawl_data.get("crawl_id")
# if not crawl_id:
#     print("❌ Error: Failed to start Firecrawl.")
#     exit()
#
# print(f"🚀 Firecrawl started! Crawl ID: {crawl_id}")
#
# # Step 2: Monitor Crawl Status
# while True:
#     status_response = requests.get(
#         f"{FIRECRAWL_STATUS_URL}/{crawl_id}",
#         headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
#     )
#     status_data = status_response.json()
#     status = status_data.get("status")
#
#     print(f"⏳ Status: {status}")
#
#     if status == "completed":
#         break
#     elif status in ["failed", "error"]:
#         print("❌ Firecrawl failed.")
#         exit()
#
#     time.sleep(5)
#
# # Step 3: Fetch Crawl Results
# results_response = requests.get(
#     f"{FIRECRAWL_RESULTS_URL}/{crawl_id}",
#     headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
# )
# results_data = results_response.json()
# articles = results_data.get("articles", [])
# print(articles)
#


"""
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer fc-54f5d81344d34207ae1ba87ac565458d' \
    -d '{
        "url": "https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide",
		"formats": [ "markdown" ],
		"onlyMainContent": true,
		"parsePDF": true,
		"maxAge": 14400000
	}'
"""

# Install with pip install firecrawl-py
import asyncio

from firecrawl import AsyncFirecrawlApp, FirecrawlApp

from dunstify import notify_cont

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def firecrawl_to_md(url) -> str:
    """Extract content from URL using Firecrawl API and convert to markdown.

    Args:
        url (str): URL to extract content from

    Returns:
        str: Markdown formatted content

    Raises:
        Exception: If API key is missing or extraction fails
    """
    if not FIRECRAWL_API_KEY:
        raise Exception("FIRECRAWL_API_KEY environment variable not set")
    notify_cont("firecrawl", f"firecrawl({url}) to markdown")

    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        response = app.scrape_url(
            url=url,
            formats=["markdown"],
            only_main_content=True,
            parse_pdf=True,
            max_age=14400000,
        )
        return response.markdown or "No content"
    except Exception as e:
        raise Exception(f"Firecrawl extraction failed for {url}: {e!s}")


async def async_firecrawl_to_md(url: str) -> str:
    """Extract content from URL using async Firecrawl API for better performance.

    Args:
        url (str): URL to extract content from

    Returns:
        str: Markdown formatted content

    Raises:
        Exception: If API key is missing or extraction fails
    """

    if not FIRECRAWL_API_KEY:
        raise Exception("FIRECRAWL_API_KEY environment variable not set")
    notify_cont("async_firecrawl", f"async_firecrawl({url}) to markdown")

    try:
        app = AsyncFirecrawlApp(api_key=FIRECRAWL_API_KEY)
        response = await app.scrape_url(
            url=url,
            formats=["markdown"],
            only_main_content=True,
            parse_pdf=True,
            max_age=14400000,
        )
        return response.markdown or "No content"
    except Exception as e:
        raise Exception(f"Async Firecrawl extraction failed for {url}: {e!s}")


async def async_test():
    """Test async Firecrawl functionality."""
    test_urls = [
        "https://news.hada.io/topic?id=22490",
        "https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram",
    ]

    for url in test_urls:
        print(f"\n=== Testing async Firecrawl for {url} ===")
        start_time = time.time()

        try:
            content = await async_firecrawl_to_md(url)
            elapsed = time.time() - start_time
            print(f"✅ Async Firecrawl: {len(content)} chars in {elapsed:.2f}s")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Async Firecrawl failed in {elapsed:.2f}s: {e}")


def sync_test():
    """Test sync Firecrawl functionality."""
    test_urls = [
        "https://news.hada.io/topic?id=22490",
        "https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram",
    ]

    for url in test_urls:
        print(f"\n=== Testing sync Firecrawl for {url} ===")
        start_time = time.time()

        try:
            content = firecrawl_to_md(url)
            elapsed = time.time() - start_time
            print(f"✅ Sync Firecrawl: {len(content)} chars in {elapsed:.2f}s")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Sync Firecrawl failed in {elapsed:.2f}s: {e}")


def main():
    """Compare sync vs async Firecrawl performance."""
    print("🚀 Testing Firecrawl Async vs Sync Performance")
    print("=" * 50)

    # Test sync version
    print("\n📋 SYNC FIRECRAWL TEST")
    sync_test()

    # Test async version
    print("\n⚡ ASYNC FIRECRAWL TEST")
    asyncio.run(async_test())

    print("\n✅ Firecrawl tests completed!")


if __name__ == "__main__":
    main()
