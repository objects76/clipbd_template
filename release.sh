#!/bin/bash
set -euo pipefail

echo "빌드 시작: template_paste"

uv sync

echo "실행 파일 빌드 중..."
uv run pyinstaller --onefile \
    --name "template_paste" \
    --distpath "$HOME/.local/bin" \
    --specpath "/tmp" \
    --clean \
    --noconfirm \
    "main.py"

template_paste
