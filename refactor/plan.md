# Refactoring Plan: Reorganize Project Structure
**Created:** 2026-01-22
**Session ID:** refactor_move_to_src_others_2026_01_22

## Initial State Analysis

### Current Architecture
The project has a flat structure with all Python files in the root directory. There are several categories of files:

1. **Core Application Files (Used by main.py)**:
   - `main.py` - Entry point
   - `ck_clipboard.py` - Clipboard operations
   - `command.py` - Command enumeration and logic
   - `config.py` - Configuration management
   - `datatype.py` - Data type detection
   - `dunstify.py` - Desktop notifications
   - `exceptions.py` - Custom exceptions
   - `llm.py` - LLM inference (OpenAI API)
   - `prompt.py` - Prompt generation and template formatting
   - `text_info2.py` - Text type detection and HTML conversion
   - `ui.py` - UI utilities (error, toast)
   - `webpage.py` - Web content extraction
   - `youtube.py` - YouTube transcript extraction
   - `cache.py` - Clipboard caching (used by youtube.py)

2. **Unused Root-Level Files (NOT in main.py dependency chain)**:
   - `meta_prompt.py` - Meta prompt generation (standalone utility)
   - `q_and_a.py` - Q&A text formatting (standalone utility)
   - `window_utils.py` - X11 window utilities (unused)

3. **Alternative Implementations (`ng/` directory)**:
   - `ng/clipbd.py` - Alternative clipboard implementation
   - `ng/copyq.py` - CopyQ clipboard manager integration
   - `ng/firecrawl_to_md.py` - Firecrawl API web extraction
   - `ng/get_browser_url.py` - Browser URL extraction
   - `ng/get_browser_url_advanced.py` - Advanced browser URL extraction
   - `ng/jina_to_md.py` - Jina Reader API web extraction
   - `ng/medium.py` - Medium article extraction
   - `ng/scraping.py` - Web scraping utilities
   - `ng/web_to_md.py` - Web to markdown conversion

4. **Utility Scripts in Subdirectories**:
   - `asset/merge_transcripts.py` - Transcript merging utility
   - `asset/reformat_transcript.py` - Transcript reformatting
   - `asset/transcript_to_srt.py` - SRT format conversion
   - `youtube/translate_srt.py` - SRT translation utility

### Current Directory Structure
```
.
├── main.py (entry point)
├── [13 core application files used by main.py]
├── [3 unused root-level files]
├── ng/
│   └── [9 alternative implementation files]
├── asset/
│   └── [3 utility scripts]
└── youtube/
    └── [1 utility script]
```

### Target Directory Structure
```
.
├── main.py (entry point)
├── [13 core application files - KEEP IN ROOT]
└── src/
    └── others/
        ├── [3 unused root-level files]
        ├── ng/
        │   └── [9 alternative implementation files]
        ├── asset/
        │   └── [3 utility scripts]
        └── youtube/
            └── [1 utility script]
```

### Problem Areas
1. **Cluttered Root**: Mixing actively used and unused/experimental files
2. **Unclear Organization**: Hard to distinguish core vs alternative implementations
3. **Maintenance Burden**: All files appear equally important despite usage differences

### Dependencies
**Files to Move (no dependencies on main.py chain)**:
- Root level: `meta_prompt.py`, `q_and_a.py`, `window_utils.py`
- Entire `ng/` directory (alternative implementations)
- Entire `asset/` directory (utility scripts)
- Entire `youtube/` directory (utility scripts)

**Files to Keep (core application dependencies)**:
- All 13 files in main.py dependency chain (see analysis above)

### Risk Assessment
**Low Risk** - Files to move are NOT imported by main.py or its dependencies:
- No import statements found in core application files
- Can be safely relocated without breaking main application
- Independent utility scripts with no reverse dependencies

## Refactoring Goal
Move all non-core files (not used by main.py) to `src/others/` while preserving directory structure for alternative implementations and utility scripts.

## Refactoring Tasks

### Phase 1: Preparation (Low Risk)
- [x] Analyze main.py dependency chain ✅
- [x] Identify unused files ✅
- [ ] **Task 1.1**: Create directory structure
  - **Risk**: None
  - **Actions**:
    - `mkdir -p src/others/ng`
    - `mkdir -p src/others/asset`
    - `mkdir -p src/others/youtube`
  - **Validation**: Verify directories exist

### Phase 2: Move Unused Root Files (Low Risk)
- [ ] **Task 2.1**: Move standalone utility files
  - **Risk**: Low - no dependencies
  - **Files**:
    - `meta_prompt.py` → `src/others/meta_prompt.py`
    - `q_and_a.py` → `src/others/q_and_a.py`
    - `window_utils.py` → `src/others/window_utils.py`
  - **Validation**: Verify files moved, check no imports broken

### Phase 3: Move Alternative Implementation Directory (Low Risk)
- [ ] **Task 3.1**: Move entire ng/ directory
  - **Risk**: Low - alternative implementations not used by main.py
  - **Action**: Move `ng/` → `src/others/ng/`
  - **Validation**: Verify all 9 files moved correctly

### Phase 4: Move Utility Script Directories (Low Risk)
- [ ] **Task 4.1**: Move asset/ utilities
  - **Risk**: Low - standalone scripts
  - **Action**: Move `asset/*.py` → `src/others/asset/`
  - **Note**: Keep `asset/template2.yaml` and other config files in original location
  - **Validation**: Verify only .py files moved, config files remain

- [ ] **Task 4.2**: Move youtube/ utilities
  - **Risk**: Low - standalone scripts
  - **Action**: Move `youtube/*.py` → `src/others/youtube/`
  - **Validation**: Verify files moved correctly

### Phase 5: Validation (Critical)
- [ ] **Task 5.1**: Test main application
  - **Risk**: Critical - verify no breakage
  - **Actions**:
    - Run syntax check: `python3 -m py_compile main.py`
    - Run import validation: `python3 -c "import main"`
    - Test with `--test` flag: `uv run main.py --test`
  - **Validation**: All checks pass, no import errors

- [ ] **Task 5.2**: Verify file locations
  - **Risk**: Low
  - **Actions**:
    - Confirm 13 core files remain in root
    - Confirm all moved files in `src/others/`
    - Check git status for moved files
  - **Validation**: Complete file accounting

### Phase 6: Documentation
- [ ] **Task 6.1**: Update CLAUDE.md
  - **Risk**: Low
  - **Actions**: Document new directory structure
  - **Validation**: Accurate documentation

## Validation Checklist
- [ ] src/others/ directory structure created
- [ ] 3 unused root files moved to src/others/
- [ ] ng/ directory moved to src/others/ng/
- [ ] asset/*.py moved to src/others/asset/ (config files remain)
- [ ] youtube/*.py moved to src/others/youtube/
- [ ] 13 core application files remain in root
- [ ] main.py runs without errors
- [ ] No broken imports
- [ ] Git status shows clean moves
- [ ] Documentation updated

## File Movement Mapping

| Before | After | Reason |
|--------|-------|--------|
| `meta_prompt.py` | `src/others/meta_prompt.py` | Unused utility |
| `q_and_a.py` | `src/others/q_and_a.py` | Unused utility |
| `window_utils.py` | `src/others/window_utils.py` | Unused X11 utility |
| `ng/` (9 files) | `src/others/ng/` | Alternative implementations |
| `asset/*.py` (3 files) | `src/others/asset/` | Utility scripts |
| `youtube/*.py` (1 file) | `src/others/youtube/` | Utility script |

## Files Remaining in Root (Core Application - 14 files)

| File | Reason |
|------|--------|
| `main.py` | Entry point |
| `cache.py` | Used by youtube.py |
| `ck_clipboard.py` | Used by main.py, datatype.py |
| `command.py` | Used by main.py, prompt.py |
| `config.py` | Used by main.py |
| `datatype.py` | Used by main.py, command.py, prompt.py |
| `dunstify.py` | Used by main.py, youtube.py |
| `exceptions.py` | Used by config.py, prompt.py, text_info2.py, webpage.py, youtube.py |
| `llm.py` | Used by main.py |
| `prompt.py` | Used by main.py |
| `text_info2.py` | Used by datatype.py, prompt.py, webpage.py |
| `ui.py` | Used by main.py, prompt.py, youtube.py |
| `webpage.py` | Used by prompt.py |
| `youtube.py` | Used by prompt.py |

## Implementation Strategy

### Conservative Approach (Recommended)
1. Create directory structure first
2. Move files in phases (root files → ng → asset → youtube)
3. Validate after each phase
4. Use `git mv` to preserve history
5. Test main application after all moves complete

## Rollback Strategy
- Git checkpoint before changes: Current commit `3f9379e`
- If validation fails: `git reset --hard 3f9379e`
- All moves tracked by git for easy revert

## Notes
- The `ng/` directory contains "next generation" or experimental implementations
- All files being moved are standalone utilities or alternative implementations
- Core application (main.py dependency chain) remains untouched in root
- This refactoring is purely organizational - no code changes required
