#!/bin/bash
set -euo pipefail

YOUTUBE_VIDEO_URL="$1"

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")

yt-dlp --write-auto-subs --convert-subs srt --sub-lang en \
    -o "$SCRIPT_DIR/%(title).48B [%(id)s].%(ext)s" \
    "$YOUTUBE_VIDEO_URL"



