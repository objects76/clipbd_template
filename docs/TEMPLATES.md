# Template System Guide

## 📋 Overview

The clipboard template system uses YAML configuration files to define content processing templates. Templates transform extracted content (YouTube transcripts, web pages, text) into structured, formatted outputs.

---

## 🏗️ Template Structure

### Basic Template Format

```yaml
TEMPLATES:
  template_name: |-
    Template content with variables and formatting instructions.

    Variables: {variable_name}

    Additional template content...
```

### Template Variables

Templates support variable substitution using Python string formatting:

| Variable | Source | Description |
|----------|---------|-------------|
| `{video_id}` | YouTube | Video ID for URL generation |
| `{transcript}` | YouTube | Video transcript text |
| `{content}` | Web/Text | Extracted content |
| `{title}` | Web/Medium | Page/article title |
| `{url}` | Web | Source URL |

---

## 📝 Built-in Templates

### YouTube Summary Template

**Template Name:** `youtube summary`

**Purpose:** Creates structured summaries of YouTube videos with timestamped navigation

**Features:**
- Korean language output
- Clickable timestamp links
- Step-by-step technical guides
- Technical terminology explanations
- Structured sections (Overview, Steps, Tips, Terminology, Conclusion)

**Example Output:**
```markdown
# YouTube Video Summary

## 개요
비디오의 주요 목표와 기술적 주제에 대한 간략한 개요 (2-3문장)

## 단계별 가이드
• [19:56](https://www.youtube.com/watch?v=VIDEO_ID&t=1196s) 첫 번째 단계 설명
• [25:30](https://www.youtube.com/watch?v=VIDEO_ID&t=1530s) 두 번째 단계 설명

## 주요 팁과 모범 사례
• 일반적인 실수를 피하는 방법
• 워크플로우 개선 조언

## 기술 용어
• **용어1**: 설명
• **용어2**: 설명

## 결론 및 결과
최종 권장사항과 달성 가능한 결과
```

### Web Page Summary Template

**Template Name:** `webpage summary`

**Purpose:** Structures web page content into organized summaries

**Features:**
- Content categorization
- Key points extraction
- Source attribution
- Structured analysis

### Meta Prompt Template

**Template Name:** `meta prompt`

**Purpose:** Converts text into structured LLM prompts

**Features:**
- Prompt optimization
- Context enhancement
- Variable identification
- Output formatting

### Q&A Context Template

**Template Name:** `Q&A on context`

**Purpose:** Formats content for question-answering workflows

**Features:**
- Context preparation
- Question generation
- Answer formatting
- Reference linking

---

## 🛠️ Creating Custom Templates

### Step 1: Define Template Structure

```yaml
TEMPLATES:
  custom_template: |-
    # Custom Template

    ## Input Analysis
    Content Type: {content_type}
    Source: {source}

    ## Processing Instructions
    {processing_instructions}

    ## Output Format
    {formatted_content}
```

### Step 2: Add Variable Support

```yaml
TEMPLATES:
  advanced_template: |-
    # Advanced Analysis Template

    **Source:** {url}
    **Title:** {title}
    **Word Count:** {word_count}

    ## Summary
    {summary}

    ## Key Points
    {key_points}

    ## Technical Details
    {technical_details}
```

### Step 3: Template Configuration

```yaml
TEMPLATES:
  configurable_template: |-
    # Configurable Output Template

    **Language:** {output_language}
    **Style:** {output_style}
    **Detail Level:** {detail_level}

    ## Content Analysis
    {analysis}

    ## Recommendations
    {recommendations}
```

---

## 🔧 Template System Configuration

### Template File Location

**Default Path:** `asset/template2.yaml`

**Configuration Path:** `~/.config/rofi/template.yaml`

### Environment-Specific Templates

```yaml
# Development templates
TEMPLATES:
  debug_output: |-
    # DEBUG: Content Analysis

    Raw Input: {raw_input}
    Content Type: {content_type}
    Processing Time: {processing_time}

    ## Processed Output
    {processed_content}

# Production templates
TEMPLATES:
  production_summary: |-
    # Content Summary

    ## Overview
    {overview}

    ## Key Information
    {key_info}
```

---

## 📊 Template Variables Reference

### YouTube Content Variables

```python
{
    "video_id": str,          # YouTube video ID
    "transcript": str,        # Full transcript text
    "duration": str,          # Video duration
    "title": str,            # Video title (if available)
    "channel": str           # Channel name (if available)
}
```

### Web Content Variables

```python
{
    "url": str,              # Source URL
    "title": str,            # Page title
    "content": str,          # Extracted content
    "source": str,           # Extraction method
    "word_count": int,       # Content word count
    "metadata": dict         # Additional metadata
}
```

### Medium Article Variables

```python
{
    "title": str,            # Article title
    "content": str,          # Cleaned content
    "markdown": str,         # Markdown format
    "author": str,           # Author name (if available)
    "publication": str       # Publication name (if available)
}
```

---

## 🎨 Advanced Template Features

### Conditional Content

```yaml
TEMPLATES:
  conditional_template: |-
    # Content Analysis

    {% if video_id %}
    **Video:** https://youtube.com/watch?v={video_id}
    {% endif %}

    {% if url %}
    **Source:** {url}
    {% endif %}

    ## Content
    {content}
```

### Multi-Language Support

```yaml
TEMPLATES:
  multilingual_template: |-
    # Content Summary / 내용 요약

    ## English Summary
    {english_summary}

    ## Korean Summary / 한국어 요약
    {korean_summary}

    ## Technical Terms / 기술 용어
    {technical_terms}
```

### Structured Output Formats

```yaml
TEMPLATES:
  json_output: |-
    ```json
    {
      "title": "{title}",
      "summary": "{summary}",
      "key_points": [
        {key_points_json}
      ],
      "metadata": {
        "source": "{url}",
        "processed_at": "{timestamp}"
      }
    }
    ```

  markdown_table: |-
    # Analysis Results

    | Field | Value |
    |-------|-------|
    | Title | {title} |
    | Source | {url} |
    | Type | {content_type} |
    | Summary | {summary} |
```

---

## 🔄 Template Processing Pipeline

### 1. Content Detection
```
Clipboard Content → Content Type Detection → Variable Extraction
```

### 2. Template Selection
```
Content Type → Auto-Selection OR Manual Selection (rofi) → Template Loading
```

### 3. Variable Substitution
```
Template + Variables → String Formatting → Processed Template
```

### 4. Output Generation
```
Processed Template → Clipboard → Auto-Paste (xdotool)
```

---

## 🧪 Testing Templates

### Manual Testing

```bash
# Test with specific template
python main.py --template ~/.config/rofi/template.yaml

# Test with auto-detection
python main.py --auto

# Debug mode
python main.py --test
```

### Template Validation

```python
import yaml

# Load and validate template
def validate_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    if 'TEMPLATES' not in config:
        raise ValueError("Missing TEMPLATES section")

    templates = config['TEMPLATES']
    for name, content in templates.items():
        if not isinstance(content, str):
            raise ValueError(f"Template '{name}' must be string")

        # Check for required variables
        if '{content}' not in content and '{transcript}' not in content:
            print(f"Warning: Template '{name}' has no content variables")

    return config
```

---

## 📋 Template Best Practices

### Content Organization
- Use clear section headers
- Include source attribution
- Maintain consistent formatting
- Add navigation elements

### Variable Usage
- Always include fallback content for optional variables
- Use descriptive variable names
- Validate variable availability

### Output Quality
- Structure content logically
- Include relevant metadata
- Optimize for readability
- Support multiple output formats

### Performance
- Keep templates concise
- Avoid complex processing in templates
- Use efficient variable substitution
- Cache frequently used templates

---

## 🔗 Integration Examples

### Rofi Integration

```bash
# Template selection with rofi
rofi -dmenu -no-custom \
    -theme-str 'window {width: 10%;} entry { enabled: false; }' \
    -p 'Choose Template:'
```

### CopyQ Integration

```python
# Get clipboard content for template processing
from copyq import get_lastest_clipboard

items = get_lastest_clipboard(n=2)
content = items[0]['data'] if items else ""
```

---

*Generated by SuperClaude /sc:index - Template Documentation System*