#!/bin/bash
set -euo pipefail

echo "빌드 시작: template_paste"

uv sync

echo "실행 파일 빌드 중..."
uv run pyinstaller --onefile \
    --name "template_paste" \
    --distpath "$HOME/.local/bin" \
    --specpath "/tmp" \
    --paths "$(pwd)/src" \
    --clean --noconfirm \
    "src/main.py"

cp -f ".env" "$HOME/.config/rofi/.env"

    # --hidden-import youtube_transcript_api \
    # --hidden-import bs4 \
    # --hidden-import lxml \
    # --hidden-import openai \
    # --hidden-import firecrawl \
    # --hidden-import transformers \
    # --hidden-import torch \
    # --add-data "$(pwd)/clipbd.py:." \
    # --add-data "$(pwd)/youtube.py:." \
    # --add-data "$(pwd)/scraping.py:." \
    # --add-data "$(pwd)/firecrawl_to_md.py:." \
    # --add-data "$(pwd)/jina_to_md.py:." \
    # --add-data "$(pwd)/medium.py:." \

template_paste
