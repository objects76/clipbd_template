# Nuitka Build Guide for clipbd-template

Complete guide for building the clipboard template application with Nuitka compilation for optimized performance and standalone distribution.

## Quick Start

```bash
# 1. Install system dependencies (Linux only)
sudo apt install patchelf         # Ubuntu/Debian
# or
sudo dnf install patchelf         # Fedora/RHEL

# 2. Install Python dependencies with Nuitka
uv sync --group dev

# 3. Build standalone executable (RECOMMENDED)
./scripts/build_nuitka.sh

# 4. Output: ~/.local/bin/template_paste (standalone executable)
```

## Build Methods

### Method 1: Standalone Executable (RECOMMENDED)

**What**: Creates a self-contained executable with all dependencies bundled.

**When**: For desktop deployment, no Python installation needed.

**Command**:
```bash
./scripts/build_nuitka.sh
```

**Output**:
- `~/.local/bin/template_paste` - Standalone executable (~50-100 MB)
- `~/.config/rofi/.env` - Environment configuration (auto-copied)

**Usage**:
```bash
template_paste --auto
template_paste --template ~/.config/rofi/template.yaml
```

**Advantages**:
- No Python runtime needed on target system
- All dependencies bundled
- Fast startup (no .pyc compilation)
- Ready for distribution

### Method 2: Module Compilation (Development)

**What**: Compiles Python modules to native .so extensions.

**When**: For development testing or when Python is available.

**Command**:
```bash
uv run python -m nuitka \
    --module \
    --include-package=ck_clipboard \
    --include-package=command \
    --include-package=config \
    --output-dir=dist/modules \
    src/main.py
```

**Output**: `dist/modules/main.cpython-311-x86_64-linux-gnu.so`

### Method 3: Wheel Package (Future)

**What**: Creates a PyPI-ready wheel with compiled modules.

**When**: For packaging and distribution via pip.

**Command**:
```bash
uv run setup.py bdist_nuitka
```

**Output**: `dist/clipbd_template-*.whl`

---

## Environment Setup

### 1. System Dependencies

#### Linux (Required for standalone builds)
```bash
# Ubuntu/Debian
sudo apt install patchelf build-essential

# Fedora/RHEL
sudo dnf install patchelf gcc gcc-c++

# Arch Linux
sudo pacman -S patchelf base-devel
```

**Why patchelf**: Required for standalone executables to bundle shared libraries.

#### macOS
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

#### Windows
Visual Studio 2022 or Build Tools. Nuitka will prompt to download MinGW64 on first run.

### 2. Python Dependencies

```bash
# Install all dependencies including Nuitka
uv sync --group dev

# Verify Nuitka installation
uv run python -m nuitka --version
# Should output: Nuitka 2.8.9 or higher
```

### 3. Runtime Dependencies

The application requires these system tools at runtime:
- `copyq` or `copykitten` - Clipboard management
- `rofi` - Template selection GUI
- `xdotool` - Keyboard automation
- `notify-send` (dunst) - Desktop notifications

```bash
# Ubuntu/Debian
sudo apt install copyq rofi xdotool dunst

# Fedora/RHEL
sudo dnf install copyq rofi xdotool dunst

# Arch Linux
sudo pacman -S copyq rofi xdotool dunst
```

---

## Build Configuration

### Optimization Options (in scripts/build_nuitka.sh)

```bash
# Performance optimizations
--lto=yes                              # Link-time optimization (+5-10% speed, -15% size)
--python-flag=no_docstrings            # Strip docstrings (-20% size)
--python-flag=no_annotations           # Strip type hints (-5% size)

# Size reduction
--enable-plugin=anti-bloat             # Remove unused imports (-10% size)

# Heavy library exclusion (keep as Python imports)
--nofollow-import-to=torch             # Don't compile PyTorch
--nofollow-import-to=transformers      # Don't compile Transformers
--nofollow-import-to=openai            # Don't compile OpenAI SDK
--nofollow-import-to=anthropic         # Don't compile Anthropic SDK

# Development tool exclusion
--nofollow-import-to=ipykernel         # Don't compile Jupyter
--nofollow-import-to=pytest            # Don't compile test frameworks
```

### Why Exclude Heavy Libraries?

**Problem**: ML libraries (torch, transformers) are:
- Already highly optimized (C/CUDA)
- Very large (100+ MB each)
- Slow to compile (10-30 minutes)
- Minimal performance gain when compiled

**Solution**: Keep them as Python imports:
- Your application code gets compiled (fast, 2-4x speedup)
- ML libraries stay as Python (fine, already fast)
- Total build time: 2-5 minutes instead of 30+ minutes
- Final size: ~50 MB instead of 200+ MB

### Package Data Inclusion

Non-Python files are automatically included via `--include-package-data`:
- `asset/template.yaml` - Template definitions
- `asset/template2.yaml` - Alternative templates
- `.env` - Environment configuration (copied separately)

---

## Build Process Details

### What Happens During Build

**Step 1: Environment Setup**
```
Clean previous builds (dist/nuitka, build/)
Create output directories
```

**Step 2: Nuitka Compilation**
```
Nuitka compiles: src/*.py → C code → native binary
Process:
  1. Parse Python AST
  2. Generate optimized C code
  3. Compile with gcc/clang (with LTO)
  4. Link dependencies into single executable
Time: 2-5 minutes
```

**Step 3: Dependency Bundling**
```
Bundle required .so files:
  - Python runtime
  - Required Python packages (copykitten, pyyaml, etc.)
  - System libraries
Result: Self-contained executable
```

**Step 4: Installation**
```
Copy executable: dist/nuitka/template_paste → ~/.local/bin/
Copy config: .env → ~/.config/rofi/.env
Set executable permissions
```

### Expected Build Output

```bash
$ ./scripts/build_nuitka.sh

🔨 Building template_paste with Nuitka...
  Project root: /home/jjkim/Desktop/work/nocode/clipbd_template
  Output directory: /home/jjkim/.local/bin

Nuitka: Starting compilation...
Nuitka: Completed module 'main' (100%)
Nuitka: Completed module 'ck_clipboard' (100%)
Nuitka: Completed module 'command' (100%)
...
Nuitka: Linking executable...

✓ Build successful!
  Executable: dist/nuitka/template_paste
  Size: 52M

  Copied .env to ~/.config/rofi/.env

✓ Installed to: /home/jjkim/.local/bin/template_paste

Run with: template_paste --auto
```

---

## Performance Expectations

### Compilation Time

| Project Size | Estimated Time |
|--------------|----------------|
| With ML exclusions (current) | 2-5 minutes |
| Without ML exclusions | 20-40 minutes |

### Runtime Performance

| Operation | Speedup |
|-----------|---------|
| Startup time | 1.5-2x faster |
| Python logic (command parsing, config) | 2-4x faster |
| YouTube transcript download | 1.1x (network-bound) |
| Web scraping | 1.1x (network-bound) |
| LLM inference | 1.0x (API-bound) |

### Binary Size

| Mode | Size |
|------|------|
| Pure Python (no compilation) | N/A (requires Python) |
| Standalone (current) | ~50-60 MB |
| Standalone (with ML compiled) | ~200+ MB |

---

## Testing the Build

### Quick Test

```bash
# After building
template_paste --version
# Should output: template_paste 1.0.0

# Test with auto mode
template_paste --auto
# Should detect clipboard content and process
```

### Integration Test

```bash
# 1. Copy a YouTube URL to clipboard
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" | xclip -selection clipboard

# 2. Run the application
template_paste --auto

# 3. Verify output
# - Should open ChatGPT
# - Should paste formatted transcript
```

### Manual Template Selection Test

```bash
# Copy text to clipboard
echo "Test content" | xclip -selection clipboard

# Run with template selection
template_paste --template ~/.config/rofi/template.yaml

# Should show rofi menu with template options
```

---

## Troubleshooting

### Issue: "patchelf not found"

**Symptom**:
```
Error: patchelf is required for standalone builds
```

**Solution**:
```bash
sudo apt install patchelf         # Ubuntu/Debian
sudo dnf install patchelf         # Fedora/RHEL
```

### Issue: "ImportError: No module named 'copykitten'"

**Symptom**: Runtime error when executable runs.

**Cause**: Copykitten not properly bundled.

**Solution**: Add explicit inclusion in build script:
```bash
--include-package=copykitten \
--include-package-data=copykitten
```

Already included in provided `scripts/build_nuitka.sh`.

### Issue: "command not found: rofi"

**Symptom**: Application fails with rofi error.

**Cause**: System dependencies not installed.

**Solution**:
```bash
sudo apt install rofi xdotool copyq dunst
```

### Issue: Large executable size (>100 MB)

**Symptom**: Executable is very large.

**Cause**: ML libraries got compiled instead of excluded.

**Solution**: Verify exclusions in `scripts/build_nuitka.sh`:
```bash
--nofollow-import-to=torch \
--nofollow-import-to=transformers \
--nofollow-import-to=openai \
--nofollow-import-to=anthropic
```

### Issue: Slow compilation (>10 minutes)

**Symptom**: Build takes very long.

**Solutions**:

**1. Use parallel compilation**:
```bash
--jobs=4  # or number of CPU cores
```

**2. Install ccache** (speeds up recompilation):
```bash
sudo apt install ccache
export PATH="/usr/lib/ccache:$PATH"
```

**3. Verify ML exclusions** (see issue above)

### Issue: "ModuleNotFoundError" at runtime

**Symptom**: Missing module error when running executable.

**Cause**: Dynamic import not detected by Nuitka.

**Solution**: Add explicit inclusion:
```bash
--include-module=missing_module
# or
--include-package=missing_package
```

### Issue: ".env file not found"

**Symptom**: API keys not loaded.

**Cause**: .env not in expected location.

**Solution**: Build script auto-copies to `~/.config/rofi/.env`. Verify:
```bash
ls -la ~/.config/rofi/.env
```

---

## Comparison with PyInstaller

### Current PyInstaller Setup (release.sh)

```bash
uv run pyinstaller --onefile \
    --name "template_paste" \
    --distpath "$HOME/.local/bin" \
    src/main.py
```

### Nuitka vs PyInstaller

| Feature | PyInstaller | Nuitka |
|---------|-------------|--------|
| Build time | 1-2 min | 2-5 min |
| Runtime speed | Same as Python | 2-4x faster |
| Startup time | Slow (extract to temp) | Fast (native) |
| Binary size | ~40-60 MB | ~50-60 MB |
| Detection | Often flagged by antivirus | Rarely flagged |
| Debugging | Difficult | Easier (native stack traces) |

### Why Switch to Nuitka?

**Advantages**:
1. **Faster execution**: Python logic runs 2-4x faster
2. **Faster startup**: No extraction step
3. **Better security**: Less likely to be flagged as malware
4. **Native debugging**: Standard gdb/lldb support

**Disadvantages**:
1. Longer build time (2x)
2. Requires C compiler
3. More complex setup

**Recommendation**: Use Nuitka for production, PyInstaller for quick testing.

---

## CI/CD Integration (Future)

### GitHub Actions Example

```yaml
name: Build Nuitka Executable

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y patchelf build-essential

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync --group dev

      - name: Build executable
        run: ./scripts/build_nuitka.sh

      - name: Test executable
        run: |
          $HOME/.local/bin/template_paste --version

      - name: Upload executable
        uses: actions/upload-artifact@v3
        with:
          name: template_paste-linux-x86_64
          path: ~/.local/bin/template_paste
```

---

## Distribution Workflow

### 1. Build for Target Platform

```bash
# Linux
./scripts/build_nuitka.sh

# macOS (on Mac)
./scripts/build_nuitka.sh

# Windows (on Windows)
./scripts/build_nuitka.bat  # Would need to create
```

### 2. Package for Distribution

```bash
# Create archive
cd ~/.local/bin
tar -czf template_paste-linux-x86_64.tar.gz template_paste

# With config
mkdir -p template_paste-dist
cp template_paste template_paste-dist/
cp ~/.config/rofi/.env template_paste-dist/.env.example
tar -czf template_paste-linux-x86_64.tar.gz template_paste-dist/
```

### 3. Create Release

```bash
# Tag version
git tag v1.0.0
git push origin v1.0.0

# Create GitHub release with executable
gh release create v1.0.0 \
    template_paste-linux-x86_64.tar.gz \
    --title "v1.0.0" \
    --notes "Initial release with Nuitka compilation"
```

---

## Best Practices

### 1. Keep ML Libraries as Python Imports

Always exclude heavy ML libraries:
```bash
--nofollow-import-to=torch
--nofollow-import-to=transformers
```

Your code gets compiled (fast), ML libs stay optimized (fine).

### 2. Use Anti-Bloat Plugin

```bash
--enable-plugin=anti-bloat
```

Automatically removes unused imports and test code.

### 3. Strip Debug Symbols

For production:
```bash
--python-flag=no_docstrings
--python-flag=no_annotations
--lto=yes
```

Reduces size by ~30% with no functional impact.

### 4. Test in Clean Environment

```bash
# Test on fresh system without Python installed
# Verifies all dependencies are properly bundled
```

### 5. Version Control Build Scripts

Commit `scripts/build_nuitka.sh` and `setup.py` to repository.

**Already done!**

---

## Quick Reference

### Build Commands

```bash
# Standalone executable (recommended)
./scripts/build_nuitka.sh

# Module compilation (development)
uv run python -m nuitka --module src/main.py

# Wheel package (future)
uv run setup.py bdist_nuitka
```

### Output Locations

- Standalone executable: `~/.local/bin/template_paste`
- Module compilation: `dist/nuitka/*.so`
- Wheel package: `dist/*.whl`
- Build artifacts: `build/` (auto-cleaned)

### Test Commands

```bash
template_paste --version
template_paste --auto
template_paste --template ~/.config/rofi/template.yaml
```

---

## Related Documentation

- [Official Nuitka Manual](https://nuitka.net/doc/user-manual.html)
- [Nuitka Standalone Guide](https://nuitka.net/doc/user-manual.html#use-case-3-standalone-executables)
- [Anti-Bloat Plugin](https://nuitka.net/info/unwanted-module.html)
- Project README: `README.md`
- Original PyInstaller build: `release.sh`

---

## Summary

### Key Points

1. **Use `./scripts/build_nuitka.sh`** for standalone executable
2. **Exclude ML libraries** for faster builds and smaller size
3. **System dependencies**: patchelf (Linux), rofi, xdotool, copyq
4. **Output**: `~/.local/bin/template_paste` (50-60 MB)
5. **Performance**: 2-4x faster Python logic, 1.5-2x faster startup

### Quick Start Again

```bash
# One-time setup
sudo apt install patchelf rofi xdotool copyq dunst
uv sync --group dev

# Build
./scripts/build_nuitka.sh

# Run
template_paste --auto
```

---

**Next Steps**:
- Test the build with your workflow
- Compare performance vs PyInstaller version
- Consider CI/CD integration for automated builds
- Package for distribution if needed
