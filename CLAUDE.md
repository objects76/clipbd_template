# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a clipboard-based content extraction and template system that processes various content types (YouTube videos, web pages, Medium articles) from the clipboard and formats them using predefined templates. The application is designed as a desktop utility that integrates with Linux desktop environments using rofi for template selection and copyq for clipboard management.

### Core Components

- **main.py**: Entry point that handles template selection via rofi interface and orchestrates content processing
- **clipbd.py**: Central clipboard processing module that extracts and processes different content types
- **scraping.py**: Web scraping orchestrator that tries multiple extraction services (Jina → Firecrawl → raw HTML)
- **Content extractors**: Specialized modules for different content types:
  - `youtube.py`: YouTube transcript extraction using youtube-transcript-api
  - `medium.py`: Medium article content extraction with HTML cleaning
  - `firecrawl_to_md.py`: Firecrawl service integration for web content
  - `jina_to_md.py`: Jina Reader API integration for web content

### Data Flow

1. Content is detected from clipboard using copyq
2. Auto-detection determines content type (YouTube URL, web URL, long text)
3. Appropriate extractor processes the content
4. Content is formatted using YAML templates from `asset/template.yaml`
5. Result is copied back to clipboard and auto-pasted using xdotool

### Template System

Templates are defined in `asset/template.yaml` with support for:
- YouTube video summaries with timestamped navigation
- Web page summaries with structured analysis
- Meta prompt conversion
- Q&A on context

## Development Commands

### Setup
```bash
# Initialize Python 3.11 environment
uv sync
uv pip install ipykernel pyinstaller
```

### Development
```bash
# Run main application with auto-detection
python main.py --auto

# Run with manual template selection
python main.py --template ~/.config/rofi/template.yaml

# Test script
python main.py --test
```

### Testing Individual Components
```bash
# Test YouTube extraction
python youtube.py

# Test clipboard functions
python clipbd.py

# Test web scraping
python scraping.py

# Test Medium extraction
python medium.py

# Test Jina API
python jina_to_md.py

# Test Firecrawl API
python firecrawl_to_md.py
```

### Build & Deploy
```bash
# Build executable using provided script
./release.sh

# Manual build command
uv run pyinstaller --onefile \
    --name template_paste \
    --distpath ~/.local/bin/ \
    --specpath /tmp/ \
    main.py
```

## Environment Configuration

The application expects a `.env` file at `~/.config/rofi/.env` with API keys:
- `JINA_API_JJKIM`: Jina Reader API key
- `JINA_API_OBJECTS76`: Alternative Jina API key  
- `FIRECRAWL_API_KEY`: Firecrawl service API key

## Dependencies & Integration

### System Dependencies
- `copyq`: Clipboard manager for content extraction
- `rofi`: GUI for template selection
- `xdotool`: Keyboard automation for pasting
- `notify-send`: Desktop notifications

### Key Python Dependencies
- `pyperclip`: Cross-platform clipboard operations
- `youtube-transcript-api`: YouTube transcript downloading
- `firecrawl-py`: Firecrawl service client
- `bs4`, `lxml`: HTML parsing for Medium articles
- `requests`: HTTP client for web scraping
- `pyyaml`: Template configuration parsing

## Error Handling Strategy

The application uses a fallback chain approach:
1. **Web scraping**: Jina Reader → Firecrawl → raw HTML requests
2. **API failures**: Multiple API keys with automatic failover
3. **Content detection**: Auto-detection with manual override option
4. **User feedback**: Desktop notifications for errors and status updates

## Notebook Development

`test.ipynb` and `ng/readerlm-v2.ipynb` are available for interactive development and testing of extraction algorithms.