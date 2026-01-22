# Refactoring Plan: Split get_prompt Function
**Created:** 2026-01-22
**Session ID:** refactor_get_prompt_2026_01_22

## Initial State Analysis

### Current Architecture
The `get_prompt` function in [prompt.py:92-101](prompt.py#L92-L101) currently performs two distinct responsibilities:

1. **Data Transformation** (`post_process` function): Converts raw clipboard data into structured content dictionaries based on data type (YouTube, web URLs, HTML, markdown, etc.)
2. **Template Formatting** (`get_template` + string formatting): Loads YAML templates and formats them with the transformed data

**Current Flow:**
```
get_prompt(template_path, command, dtype, data)
  ├─> get_template(template_path, command, dtype) → template string
  ├─> post_process(dtype, data) → content dict
  └─> template.format(**content) → final formatted prompt
```

### Problem Areas
1. **Mixed Responsibilities**: Single function handles both data transformation and template formatting
2. **Tight Coupling**: Template selection logic embedded within prompt generation
3. **Reusability**: Cannot reuse data transformation without template formatting
4. **Testing Complexity**: Hard to test data transformation separately from template formatting

### Dependencies
**Internal:**
- `youtube.get_youtube_content()` - YouTube transcript extraction
- `webpage.get_html_from_url()` - Web content fetching
- `webpage.from_html_text()` - HTML text processing
- `text_info2.html_to_md()` - HTML to markdown conversion

**External Callers:**
- [main.py:45](main.py#L45): `prompt = get_prompt(args.template, command, dtype, data)`

**Template File:**
- `asset/template2.yaml` - Contains 8 templates (youtube summary, webtext summary, q&a, image analysis, translation variants)

### Test Coverage
- Manual testing in `__main__` block with YouTube URL test
- No formal unit tests detected

## Refactoring Goal
Split `get_prompt` into two focused functions:
1. **`transform_data(dtype: Datatype, data: str | Any) -> dict`** - Pure data transformation
2. **`format_with_template(template_path: str, command: Command, dtype: Datatype, content: dict) -> dict`** - Template loading and formatting

## Refactoring Tasks

### Phase 1: Extract Data Transformation (Low Risk)
- [x] **Task 1.1**: Extract `post_process` as standalone `transform_data` function
  - **Risk**: Low - function already exists, just needs promotion
  - **Changes**: Move from internal helper to top-level function
  - **Validation**: Verify return types match existing usage

### Phase 2: Create Template Formatting Function (Medium Risk)
- [ ] **Task 2.1**: Create `format_with_template` function
  - **Risk**: Medium - new function combining existing logic
  - **Changes**: Wrap `get_template` + string formatting logic
  - **Validation**: Ensure template selection logic preserved

### Phase 3: Update get_prompt to Orchestrate (High Risk - Breaking Change)
- [ ] **Task 3.1**: Refactor `get_prompt` to call new functions
  - **Risk**: High - changes external API behavior
  - **Changes**: Update function body to orchestrate `transform_data` + `format_with_template`
  - **Validation**: Run manual test in `__main__` block

### Phase 4: Update Callers (Critical)
- [ ] **Task 4.1**: Update [main.py:45](main.py#L45) caller
  - **Risk**: Critical - application entry point
  - **Changes**: May need to handle new return structure
  - **Validation**: Full application smoke test

### Phase 5: Documentation & Cleanup
- [ ] **Task 5.1**: Update function docstrings
- [ ] **Task 5.2**: Update API documentation in `docs/API.md`
- [ ] **Task 5.3**: Add type hints for all new/modified functions

## Validation Checklist
- [ ] All old patterns removed (no duplicate logic)
- [ ] No broken imports
- [ ] Manual test in `__main__` passes
- [ ] Application runs end-to-end without errors
- [ ] Type checking clean (Python 3.10+ syntax)
- [ ] No orphaned code
- [ ] Documentation updated

## De-Para Mapping (Function Signatures)

| Before | After | Status |
|--------|-------|--------|
| `get_prompt(template_path, command, dtype, data) -> dict` | `get_prompt(template_path, command, dtype, data) -> dict` | Pending - internal refactor |
| `post_process(dtype, data) -> dict \| None` | `transform_data(dtype, data) -> dict \| None` | Pending |
| N/A | `format_with_template(template_path, command, dtype, content) -> dict` | Pending - new |

## Implementation Strategy

### Approach 1: Conservative (Recommended)
1. Keep `get_prompt` signature unchanged for backward compatibility
2. Extract internal functions as described
3. `get_prompt` becomes orchestrator calling new functions
4. Low risk to existing callers

### Approach 2: Breaking Change
1. Remove `get_prompt` entirely
2. Force callers to use `transform_data` + `format_with_template` directly
3. Higher risk, better separation of concerns

**Recommendation**: Use Approach 1 to minimize risk and maintain backward compatibility.

## Rollback Strategy
- Git checkpoint before changes: `git commit -m "chore: checkpoint before get_prompt refactor"`
- If validation fails, revert to checkpoint
- Keep original function logic commented out during initial testing

## Notes
- The `post_process` function already exists and performs clean data transformation
- Template formatting is simple string `.format()` call - minimal complexity
- Main risk is ensuring all data flow paths are preserved
