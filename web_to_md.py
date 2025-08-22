import html_to_markdown

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
    # Try Jina Reader API first
    try:
        markdown = html_to_markdown.convert_to_markdown(
            html,
            extract_metadata = False,
            )
        # Compress SVG images to reduce size
        compressed_markdown = compress_md(markdown)
        print(f"html to markdown: {len(html)} -> {len(markdown)} -> {len(compressed_markdown)} (compressed)")
        return compressed_markdown
    except Exception as e:
        raise Exception(f"html to markdown: {str(e)}")

