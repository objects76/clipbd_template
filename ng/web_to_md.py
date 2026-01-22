#!/usr/bin/env python3
"""
Enhanced web content extraction with parallel processing and fallback chain.

This module provides both synchronous and asynchronous web content extraction
with intelligent fallback mechanisms for maximum reliability and performance.
"""

import asyncio
import time
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from firecrawl_to_md import async_firecrawl_to_md, firecrawl_to_md
from jina_to_md import jina_to_md

load_dotenv()

API_CALL_TIMEOUT = 120  # seconds


@dataclass
class ExtractionResult:
    """Structured result from content extraction methods."""

    method: str  # extraction method name ('jina', 'firecrawl', 'html')
    content: str | None  # extracted content (None if failed)
    content_type: str  # content format ('Markdown', 'HTML')
    error: str | None = None  # error message if extraction failed

    @property
    def success(self) -> bool:
        """Check if extraction was successful."""
        return self.content is not None and self.error is None

    @property
    def content_length(self) -> int:
        """Get content length safely."""
        return len(self.content) if self.content else 0

    @property
    def is_vaild_md(self) -> bool:
        """Check if result contains valid, substantial Markdown content."""
        return (
            self.content_length > 200
            and self.content_type == "Markdown"
            and self.content is not None
        )

    def __str__(self) -> str:
        """String representation for logging."""
        if self.success:
            return f"{self.method} result ({self.content_length} chars, {self.content_type} format)"
        return f"{self.method} failed: {self.error}"


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
            timeout=API_CALL_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ClipboardTemplate/1.0)"},
        )
        response.raise_for_status()
        return response.text
    if parsed.scheme == "file":
        with open(parsed.path, encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")


async def parallel_extraction(url: str) -> tuple[str, str]:
    """Extract content using parallel processing and select the longer result.

    Runs Jina API, Firecrawl API, and raw HTML extraction in parallel and returns
    the longer (more comprehensive) result. Longer content typically indicates
    better extraction quality and completeness.

    Args:
        url (str): URL to extract content from

    Returns:
        Tuple[str, str]: (format, content) where format is 'Markdown' or 'HTML'

    Raises:
        Exception: If all parallel extraction methods fail
    """
    with open("web_to_md.md", "w") as f:
        f.write(f"\n\n\n# {url}\n")

    async def async_jina_extraction() -> ExtractionResult:
        """Async wrapper for Jina API extraction."""
        loop = asyncio.get_event_loop()
        try:
            print(f"jina_to_md({url})")  # debug
            content = await loop.run_in_executor(None, jina_to_md, url)
            return ExtractionResult(
                method="jina", content=content, content_type="Markdown"
            )
        except Exception as e:
            return ExtractionResult(
                method="jina", content=None, content_type="Markdown", error=str(e)
            )

    async def async_firecrawl_extraction() -> ExtractionResult:
        """Native async Firecrawl API extraction for optimal performance."""
        try:
            print(f"async_firecrawl_to_md({url})")  # debug
            content = await async_firecrawl_to_md(url)
            return ExtractionResult(
                method="firecrawl", content=content, content_type="Markdown"
            )
        except Exception as e:
            return ExtractionResult(
                method="firecrawl", content=None, content_type="Markdown", error=str(e)
            )

    async def async_html_extraction() -> ExtractionResult:
        """Async wrapper for raw HTML extraction."""
        loop = asyncio.get_event_loop()
        try:
            print(f"get_html({url})")  # debug
            content = await loop.run_in_executor(None, get_html, url)
            return ExtractionResult(method="html", content=content, content_type="HTML")
        except Exception as e:
            return ExtractionResult(
                method="html", content=None, content_type="HTML", error=str(e)
            )

    # Create parallel tasks for all three extraction methods
    tasks = [
        asyncio.create_task(async_jina_extraction()),
        asyncio.create_task(async_firecrawl_extraction()),
        asyncio.create_task(async_html_extraction()),
    ]

    errors = []
    successful_results = []

    try:
        # Wait for all tasks to complete or timeout
        done, pending = await asyncio.wait(
            tasks, timeout=API_CALL_TIMEOUT, return_when=asyncio.ALL_COMPLETED
        )

        # Cancel any remaining tasks (shouldn't be any with ALL_COMPLETED)
        for task in pending:
            task.cancel()
            errors.append("Task timed out")

        # Collect all results using dataclass
        for task in done:
            try:
                result: ExtractionResult = await task
                if result.success:
                    successful_results.append(result)
                    with open("web_to_md.md", "a") as f:
                        f.write(f"\n\n\n# {result!s}\n")
                        f.write(f"{result.content}\n")
                else:
                    errors.append(str(result))  # Uses __str__ method
                    print(f"failed: {result!s}")  # debug
            except Exception as e:
                print(f"Task execution failed: {e!s}")  # debug
                errors.append(f"Task execution failed: {e!s}")

        # Select the longer result if we have successful extractions
        if successful_results:
            # Sort by content length (descending) and take the longest
            successful_results.sort(key=lambda x: x.content_length, reverse=True)
            best_result = successful_results[0]
            # Enhanced result selection: prefer valid Markdown over just length
            if not best_result.is_vaild_md and len(successful_results) > 1:
                for candidate in successful_results[1:]:
                    if candidate.is_vaild_md:
                        print(
                            f"Switching to {candidate.method} - better Markdown content"
                        )
                        best_result = candidate
                        break

            print(f"Selected {best_result}")  # Uses __str__ method
            return best_result.content_type, best_result.content

    except Exception as e:
        errors.append(f"Parallel execution failed: {e!s}")

    raise Exception(
        f"All parallel extraction methods failed for {url}: {'; '.join(errors)}"
    )


def crawling_sync(url: str) -> tuple[str, str]:
    """Extract content from URL using sequential fallback chain.

    This is the original synchronous implementation that tries methods in sequence.

    Args:
        url (str): URL to extract content from

    Returns:
        Tuple[str, str]: (format, content) where format is 'Markdown' or 'HTML'

    Raises:
        ValueError: If URL format is invalid
        Exception: If all extraction methods fail
    """
    if not url.startswith(("https:", "http:")):
        raise ValueError(f"Invalid URL format: {url}")

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

    # Final fallback to raw HTML
    try:
        content = get_html(url)
        return "HTML", content
    except Exception as e:
        errors.append(f"Raw HTML extraction failed: {e!s}")
        raise Exception(f"All extraction methods failed for {url}: {'; '.join(errors)}")


async def crawling_async(url: str) -> tuple[str, str]:
    """Extract content from URL using parallel processing with HTML fallback.

    This enhanced version tries parallel API extraction first, then falls back
    to raw HTML if both APIs fail.

    Args:
        url (str): URL to extract content from

    Returns:
        Tuple[str, str]: (format, content) where format is 'Markdown' or 'HTML'

    Raises:
        ValueError: If URL format is invalid
        Exception: If all extraction methods fail
    """
    if not url.startswith(("https:", "http:")):
        raise ValueError(f"Invalid URL format: {url}")

    errors = []

    # Try parallel API extraction first
    try:
        return await parallel_extraction(url)
    except Exception as e:
        errors.append(f"Parallel API extraction failed: {e!s}")


def crawling(url: str, use_parallel: bool = True) -> tuple[str, str]:
    """Extract content from URL with optional parallel processing.

    Main entry point that chooses between parallel and sequential extraction.

    Args:
        url (str): URL to extract content from
        use_parallel (bool): Whether to use parallel processing (default: True)

    Returns:
        Tuple[str, str]: (format, content) where format is 'Markdown' or 'HTML'

    Raises:
        ValueError: If URL format is invalid
        Exception: If all extraction methods fail
    """
    if use_parallel:
        try:
            # Use asyncio to run the async version
            return asyncio.run(crawling_async(url))
        except Exception as e:
            # Fall back to sync version if async fails
            print(f"Async extraction failed, falling back to sync: {e}")
            return crawling_sync(url)
    else:
        return crawling_sync(url)


from html_to_markdown import convert_to_markdown


def html_to_md(url: str) -> str:
    html = get_html(url)
    markdown = convert_to_markdown(
        html,
        extract_metadata=False,
    )
    return markdown


test_urls = [
    "https://news.hada.io/topic?id=22490",
    # "https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram"
]


async def test_async():
    """Test async extraction functionality."""
    for url in test_urls:
        print(f"\n=== Testing async extraction for {url} ===")
        start_time = time.time()

        try:
            format_type, content = await crawling_async(url)
            elapsed = time.time() - start_time
            print(
                f"✅ Success: {format_type} content ({len(content)} chars) in {elapsed:.2f}s"
            )
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Failed in {elapsed:.2f}s: {e}")


def test_sync():
    """Test sync extraction functionality."""
    for url in test_urls:
        print(f"\n=== Testing sync extraction for {url} ===")
        start_time = time.time()

        try:
            format_type, content = crawling_sync(url)
            elapsed = time.time() - start_time
            print(
                f"✅ Success: {format_type} content ({len(content)} chars) in {elapsed:.2f}s"
            )
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Failed in {elapsed:.2f}s: {e}")


def test_parallel():
    """Test parallel extraction functionality."""
    for url in test_urls:
        print(f"\n=== Testing parallel extraction for {url} ===")
        start_time = time.time()

        try:
            format_type, content = crawling(url, use_parallel=True)
            elapsed = time.time() - start_time
            print(
                f"✅ Success: {format_type} content ({len(content)} chars) in {elapsed:.2f}s"
            )
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Failed in {elapsed:.2f}s: {e}")


def test_dataclass():
    """Test the ExtractionResult dataclass functionality."""
    print("\n🧪 DATACLASS STRUCTURE TEST")

    # Test successful result
    success_result = ExtractionResult(
        method="jina",
        content="# Sample Content\n\nThis is test content.",
        content_type="Markdown",
    )

    # Test failed result
    error_result = ExtractionResult(
        method="firecrawl",
        content=None,
        content_type="Markdown",
        error="API key not found",
    )

    print(f"✅ Success result: {success_result}")
    print(f"❌ Error result: {error_result}")
    print(f"📏 Content length: {success_result.content_length} chars")
    print(f"🎯 Success status: {success_result.success}")
    print(f"🚫 Error status: {error_result.success}")


if __name__ == "__main__":
    """Test all extraction methods and compare performance."""
    print("🚀 Testing Enhanced Web Content Extraction Methods")
    print("=" * 60)

    print("🎯 NEW FEATURES:")
    print(
        "  • Structured ExtractionResult dataclass with method/content/content_type fields"
    )
    print("  • Jina Reader API (Markdown)")
    print("  • Firecrawl API (Markdown)")
    print("  • Raw HTML extraction (HTML)")
    print("  • Smart selection: Picks the LONGEST result automatically")
    print("=" * 60)

    # Test dataclass functionality
    test_dataclass()

    # Test synchronous extraction
    # print("\n📋 SYNC EXTRACTION TEST (Sequential fallback)")
    # test_sync()

    # Test parallel extraction
    # print("\n⚡ PARALLEL EXTRACTION TEST (3 methods simultaneously)")
    # test_parallel()

    # Test pure async extraction
    print("\n🔄 ASYNC EXTRACTION TEST (3 methods with smart selection)")
    asyncio.run(test_async())

    print("\n✅ All tests completed!")
    print("\n💡 TIP: Now using structured ExtractionResult dataclass for cleaner code!")
    print("   Fields: method, content, content_type, error, success, content_length")
