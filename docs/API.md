# Clipboard Template System - API Documentation

## 📚 Table of Contents

- [Content Processing API](#content-processing-api)
- [Extraction Services API](#extraction-services-api) 
- [Clipboard Integration API](#clipboard-integration-api)
- [Template System API](#template-system-api)
- [Error Handling](#error-handling)
- [Data Structures](#data-structures)

---

## Content Processing API

### clipbd.py

Core clipboard processing module with auto-detection and content classification.

#### `get_youtube_content(test_url=None) -> dict`

Extracts YouTube video content from clipboard.

**Parameters:**
- `test_url` (str, optional): Test URL for development/testing

**Returns:**
```python
{
    "video_id": str,          # YouTube video ID
    "transcript": str         # Video transcript text
}
```

**Raises:**
- `ValueError`: No valid clipboard data found

**Usage:**
```python
content = get_youtube_content()
print(f"Video ID: {content['video_id']}")
print(f"Transcript: {content['transcript'][:100]}...")
```

#### `get_prompt() -> dict`

Extracts prompt text from clipboard for meta-prompt conversion.

**Returns:**
```python
{
    "source_prompt": str      # Raw prompt text from clipboard
}
```

#### `get_QandA() -> dict`

Extracts Q&A context from clipboard.

**Returns:**
```python
{
    "qa_context": str         # Context text for Q&A processing
}
```

#### `get_medium() -> dict`

Processes Medium article content from clipboard HTML.

**Returns:**
```python
{
    "title": str,             # Article title
    "content": str,           # Cleaned article content
    "markdown": str           # Markdown-formatted content
}
```

#### `get_longtext(text=None) -> dict`

Processes long text content from clipboard.

**Parameters:**
- `text` (str, optional): Override text input

**Returns:**
```python
{
    "content": str,           # Long text content
    "word_count": int,        # Word count
    "summary": str            # Brief summary
}
```

#### `get_webpage(test_url=None) -> dict`

Extracts web page content using scraping chain.

**Parameters:**
- `test_url` (str, optional): Test URL for development

**Returns:**
```python
{
    "url": str,               # Source URL
    "title": str,             # Page title
    "content": str,           # Extracted content
    "source": str             # Extraction method used
}
```

---

## Extraction Services API

### youtube.py

YouTube transcript extraction and processing.

#### `get_youtube_videoid(url: str) -> str`

Extracts YouTube video ID from various URL formats.

**Parameters:**
- `url` (str): YouTube URL

**Returns:**
- `str`: YouTube video ID

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

#### `download_transcript(video_id: str, language_code: str = 'ko') -> str`

Downloads transcript for YouTube video.

**Parameters:**
- `video_id` (str): YouTube video ID
- `language_code` (str): Language code (default: 'ko')

**Returns:**
- `str`: Formatted transcript with timestamps

**Raises:**
- `Exception`: Transcript not available or video not found

#### `ts_format(ts: float) -> str`

Formats timestamp for YouTube URL navigation.

**Parameters:**
- `ts` (float): Timestamp in seconds

**Returns:**
- `str`: Formatted timestamp (e.g., "19:56")

### jina_to_md.py

Jina Reader API integration for web content extraction.

#### `jina_to_md(target_url: str) -> str`

Converts web page to markdown using Jina Reader API.

**Parameters:**
- `target_url` (str): Target web page URL

**Returns:**
- `str`: Markdown-formatted content

**Environment Variables:**
- `JINA_API_JJKIM`: Primary Jina API key
- `JINA_API_OBJECTS76`: Fallback Jina API key

**API Endpoint:** `https://r.jina.ai/{url}`

### firecrawl_to_md.py

Firecrawl service integration for web content extraction.

#### `firecrawl_to_md(url: str) -> str`

Converts web page to markdown using Firecrawl service.

**Parameters:**
- `url` (str): Target web page URL

**Returns:**
- `str`: Markdown-formatted content

**Environment Variables:**
- `FIRECRAWL_API_KEY`: Firecrawl API key

**Configuration:**
```python
{
    'formats': ['markdown'],
    'includeTags': ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    'excludeTags': ['nav', 'footer', 'header', '.sidebar']
}
```

### scraping.py

Web scraping orchestrator with fallback chain.

#### `crawling(url: str) -> str`

Extracts web content using fallback chain.

**Parameters:**
- `url` (str): Target web page URL

**Returns:**
- `str`: Extracted content in markdown format

**Fallback Chain:**
1. **Jina Reader API** - Primary extraction method
2. **Firecrawl Service** - Secondary extraction method  
3. **Raw HTML + Readability** - Final fallback method

#### `get_html(url: str) -> str`

Fetches raw HTML content from URL.

**Parameters:**
- `url` (str): Target URL

**Returns:**
- `str`: Raw HTML content

**Headers:**
```python
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

### medium.py

Medium article content extraction and cleaning.

#### `extract_medium(html_content: str) -> dict`

Extracts and cleans Medium article content.

**Parameters:**
- `html_content` (str): Raw HTML content from Medium

**Returns:**
```python
{
    "title": str,             # Article title
    "content": str,           # Cleaned HTML content
    "text": str               # Plain text content
}
```

#### `compress_medium(node) -> tuple[str, str]`

Cleans and compresses Medium article HTML.

**Parameters:**
- `node`: BeautifulSoup HTML node

**Returns:**
- `tuple[str, str]`: (cleaned_html, plain_text)

**Cleaning Process:**
1. Remove scripts, styles, and comments
2. Unwrap disallowed tags
3. Strip unnecessary attributes
4. Drop empty tags
5. Compress whitespace

---

## Clipboard Integration API

### copyq.py

CopyQ clipboard manager integration.

#### `get_lastest_clipboard(n: int, debug: bool = False) -> list[dict]`

Retrieves latest clipboard items from CopyQ.

**Parameters:**
- `n` (int): Number of items to retrieve
- `debug` (bool): Enable debug output

**Returns:**
```python
[
    {
        "type": str,          # "text" or "image" 
        "data": str           # Clipboard content
    }
]
```

#### `copyq_read(row: int) -> str`

Reads specific clipboard item from CopyQ.

**Parameters:**
- `row` (int): Row number (0-based)

**Returns:**
- `str`: Clipboard content

#### `clear_lastest_clipboard(n: int = 3) -> None`

Clears latest clipboard items.

**Parameters:**
- `n` (int): Number of items to clear

---

## Template System API

### main.py

Template selection and processing system.

#### `get_template(template_path: str, choice: str = None) -> tuple[str, dict]`

Loads and selects template from YAML configuration.

**Parameters:**
- `template_path` (str): Path to template YAML file
- `choice` (str, optional): Template choice (triggers rofi if None)

**Returns:**
- `tuple[str, dict]`: (template_name, template_config)

**Template Structure:**
```yaml
TEMPLATES:
  template_name: |-
    Template content with variables...
    Variables: {variable_name}
```

#### `auto_selector() -> str`

Automatically selects appropriate template based on clipboard content.

**Returns:**
- `str`: Selected template name

**Selection Logic:**
1. Check for YouTube URLs → "youtube summary"
2. Check for web URLs → "webpage summary"  
3. Check for long text → "longtext analysis"
4. Default → manual selection

#### `resource_path(name: str) -> Path`

Resolves resource path for packaged executable.

**Parameters:**
- `name` (str): Resource filename

**Returns:**
- `Path`: Resolved resource path

---

## Error Handling

### Exception Classes

#### `CopyQError(Exception)`
Raised when CopyQ clipboard operations fail.

**Common Causes:**
- CopyQ not running
- Insufficient permissions
- Empty clipboard

#### `MediumError(Exception)`  
Raised when Medium article processing fails.

**Common Causes:**
- Invalid HTML structure
- Missing content elements
- Parsing errors

#### `DunstifyError(RuntimeError)`
Raised when desktop notification system fails.

**Common Causes:**
- dunst not running
- GUI session not available
- Permission denied

### Error Recovery Patterns

#### API Failover Chain
```python
try:
    content = jina_to_md(url)
except Exception:
    try:
        content = firecrawl_to_md(url)  
    except Exception:
        content = get_html(url)  # Raw HTML fallback
```

#### Multiple API Keys
```python
api_keys = [
    os.getenv('JINA_API_JJKIM'),
    os.getenv('JINA_API_OBJECTS76')
]

for api_key in api_keys:
    if api_key:
        try:
            return make_api_call(url, api_key)
        except Exception:
            continue
```

---

## Data Structures

### Clipboard Item Structure
```python
{
    "type": "text" | "image",     # Content type
    "data": str,                  # Content data
    "timestamp": datetime,        # When copied (internal)
    "size": int                   # Content size (internal)
}
```

### Template Configuration
```python
{
    "TEMPLATES": {
        "template_name": str,     # Template content
        "variables": dict,        # Template variables
        "metadata": dict          # Template metadata
    }
}
```

### Content Extraction Result
```python
{
    "content": str,               # Extracted content
    "title": str,                 # Content title
    "url": str,                   # Source URL
    "source": str,                # Extraction method
    "metadata": dict,             # Additional metadata
    "timestamp": datetime         # Extraction time
}
```

---

## Usage Examples

### Basic YouTube Processing
```python
from clipbd import get_youtube_content
from main import get_template

# Extract YouTube content
content = get_youtube_content()
print(f"Processing video: {content['video_id']}")

# Load template
template_name, template_config = get_template('template.yaml', 'youtube summary')

# Format content
formatted = template_config.format(**content)
```

### Web Content Extraction
```python
from scraping import crawling
from clipbd import get_webpage

# Auto-detect and extract
webpage_data = get_webpage()
print(f"Extracted from: {webpage_data['url']}")
print(f"Method used: {webpage_data['source']}")
```

### Manual Template Selection
```python
from main import get_template

# Will show rofi selection menu
template_name, template_config = get_template('template.yaml')
print(f"Selected template: {template_name}")
```

---

*Generated by SuperClaude /sc:index - API Documentation System*