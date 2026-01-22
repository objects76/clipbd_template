# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a clipboard-based content extraction and template system that processes various content types (YouTube videos, web pages, Medium articles) from the clipboard and formats them using predefined templates. The application is designed as a desktop utility that integrates with Linux desktop environments using rofi for template selection and copyq/copykitten for clipboard management.

### Core Components

- **main.py**: Entry point that handles template selection via rofi interface and orchestrates content processing
- **Content extractors**: Specialized modules for different content types:
  - `youtube.py`: YouTube transcript extraction using youtube-transcript-api
  - `webpage.py`: Web content extraction with HTML-to-markdown conversion
- **Clipboard management**:
  - `ck_clipboard.py`: Primary clipboard interface using copykitten
  - `cache.py`: Clipboard caching system for failed operations
- **Template processing**: `config.py` loads YAML templates and configuration
- **Content type detection**: `text_info2.py` classifies content (HTML, markdown, plain text)

### Alternative Implementations & Utilities

Alternative implementations and utility scripts are organized in `src/others/`:
- **src/others/ng/**: Alternative web scraping implementations (jina, firecrawl, medium extraction)
- **src/others/asset/**: Transcript processing utilities (merge, reformat, convert to SRT)
- **src/others/youtube/**: SRT translation utilities
- **src/others/**: Standalone utilities (meta_prompt.py, q_and_a.py, window_utils.py)

### Data Flow Architecture

1. **Content Detection**: clipboard data retrieved via copykitten/copyq with type classification
2. **Auto-Detection**: `get_command()` in main.py determines content type (YouTube URL, web URL, long text, image)
3. **Content Processing**: Appropriate extractor processes the content based on detected type
4. **Template Formatting**: Content formatted using YAML templates (supports variable substitution)
5. **Output Delivery**: Result copied to clipboard and auto-pasted to target application (ChatGPT)

### Template System

Templates are defined in `asset/template.yaml` with support for:
- YouTube video summaries with timestamped navigation
- Web page summaries with structured analysis
- Meta prompt conversion
- Q&A on context
- Image analysis workflows

## Project Structure

```
.
├── main.py                    # Application entry point
├── cache.py                   # Clipboard caching
├── ck_clipboard.py            # Clipboard interface
├── command.py                 # Command definitions
├── config.py                  # Configuration management
├── datatype.py                # Data type detection
├── dunstify.py                # Desktop notifications
├── exceptions.py              # Custom exceptions
├── llm.py                     # LLM inference
├── prompt.py                  # Prompt generation
├── text_info2.py              # Text classification
├── ui.py                      # UI utilities
├── webpage.py                 # Web content extraction
├── youtube.py                 # YouTube transcript extraction
├── asset/                     # Templates and configs
│   ├── template.yaml          # Template definitions
│   └── template2.yaml         # Alternative templates
├── ng/                        # Non-Python experimental files
│   ├── readerlm-v2.ipynb      # Notebook experiments
│   └── get_url_from_broswer.sh
└── src/others/                # Alternative implementations & utilities
    ├── meta_prompt.py         # Meta prompt utility
    ├── q_and_a.py             # Q&A formatting utility
    ├── window_utils.py        # X11 window utilities
    ├── ng/                    # Alternative web extractors
    │   ├── clipbd.py
    │   ├── copyq.py
    │   ├── firecrawl_to_md.py
    │   ├── get_browser_url.py
    │   ├── get_browser_url_advanced.py
    │   ├── jina_to_md.py
    │   ├── medium.py
    │   ├── scraping.py
    │   └── web_to_md.py
    ├── asset/                 # Transcript utilities
    │   ├── merge_transcripts.py
    │   ├── reformat_transcript.py
    │   └── transcript_to_srt.py
    └── youtube/               # Translation utilities
        └── translate_srt.py
```

**Core files** (root level): Actively used by main.py application
**src/others/**: Alternative implementations, experimental code, and standalone utilities not used by main application

## Development Commands

### Environment Setup
```bash
# Initialize Python 3.11 environment with uv
uv sync

# Additional development tools (optional)
uv pip install ipykernel pyinstaller
```

### Running the Application
```bash
# Run with auto-detection (opens ChatGPT automatically)
uv run main.py --auto

# Run with manual template selection via rofi
uv run main.py --template ~/.config/rofi/template.yaml

# Test mode with countdown
uv run main.py --test
```

### Testing Individual Components
```bash
# Test YouTube transcript extraction
uv run youtube.py

# Test web page content extraction
uv run webpage.py

# Test text type detection
uv run text_info2.py

# Test clipboard operations
uv run ck_clipboard.py

# Test configuration loading
uv run config.py

# Test individual processors
uv run meta_prompt.py
uv run q_and_a.py
```

### Build & Deploy
```bash
# Build executable using provided script
./release.sh

# The script copies .env to ~/.config/rofi/.env and builds to ~/.local/bin/template_paste
```

## Environment Configuration

The application expects a `.env` file at `~/.config/rofi/.env` with API keys:
- `JINA_API_JJKIM`: Jina Reader API key  
- `JINA_API_OBJECTS76`: Alternative Jina API key
- `FIRECRAWL_API_KEY`: Firecrawl service API key

Configuration options in `asset/template.yaml`:
- `clipbd_transcript`: Whether to use clipboard transcript cache
- `clear_generated`: Whether to clear clipboard after generation

## Dependencies & Integration

### System Dependencies
- `copyq`: Clipboard manager for content extraction (fallback)
- `rofi`: GUI for template selection
- `xdotool`: Keyboard automation for pasting
- `notify-send`: Desktop notifications
- `copykitten`: Primary clipboard management library

### Key Python Dependencies
- `copykitten`: Advanced clipboard operations with image support
- `youtube-transcript-api`: YouTube transcript downloading with multi-language support
- `html-to-markdown`: HTML content conversion with SVG compression
- `bs4`, `lxml`: HTML parsing and content extraction
- `firecrawl-py`: Firecrawl service client (ng/ modules)
- `requests`: HTTP client for direct web scraping
- `pyyaml`: Template configuration parsing

## Content Processing Architecture

### Content Type Detection Flow
1. **URL Detection**: Regex pattern matching for HTTP/HTTPS URLs
2. **Content Classification**: `text_info2.py` analyzes text format (HTML, markdown, plain)
3. **Source-Specific Processing**:
   - YouTube: Extract video ID → download transcript → format with timestamps
   - Web pages: HTML → cleaned content → markdown conversion
   - Long text: Direct processing with format detection

### Error Handling & Caching
- **Clipboard caching**: Failed operations cached for retry (see `cache.py`)
- **API failover**: Multiple API keys with automatic switching
- **Graceful degradation**: Raw HTML fallback when APIs fail
- **User feedback**: Desktop notifications for status and errors

## Content Extraction Details

### YouTube Processing (`youtube.py:82-95`)
- Video ID extraction from multiple URL formats
- Transcript download with language preference (en, ko)
- Timestamp formatting and segment merging
- Caching failed attempts for manual retry

### Web Content Processing (`webpage.py:103-116`)
- Medium article detection and content extraction
- SVG compression to reduce content size
- HTML-to-markdown conversion with cleaning
- Configurable content filtering

### Template Variable Substitution
Templates use Python `.format()` syntax with extracted content dictionaries:
- `{video_id}`, `{transcript}` for YouTube content
- `{content_text}`, `{source_url}` for web content  
- `{context}`, `{user_query}` for Q&A templates

## Development Environment

Interactive development available through:
- `test.ipynb`: Main development notebook for algorithm testing
- `ng/readerlm-v2.ipynb`: Advanced extraction algorithm development
- Individual module testing via `if __name__ == '__main__'` blocks

## Type Hinting

When adding type hints, use Python 3.10+ style: `list[str]`, `dict[str, int]`, `str | None` instead of `List[str]`, `Dict[str, int]`, `Optional[str]`.