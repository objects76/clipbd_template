import re
import html_to_markdown


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
    return compressed



def compress_md(md: str) -> str:
    """Compress markdown by removing or truncating long SVG images.

    Args:
        md (str): Original markdown content

    Returns:
        str: Compressed markdown with SVG images trimmed
    """
    import re

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


if __name__ == "__main__":
    with open("asset/input.html", "r") as f:
        html = f.read()
    print(html_to_md(html))
