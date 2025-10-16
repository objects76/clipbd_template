#!/usr/bin/env python3
"""
Convert merged transcript to SRT format.
Each timestamp becomes an SRT subtitle entry with English and Korean text.
"""

import re
from pathlib import Path

def parse_timestamp(timestamp: str) -> tuple[int, int]:
    """Convert timestamp like '0:17' to minutes and seconds."""
    parts = timestamp.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1])
    return minutes, seconds

def format_srt_time(minutes: int, seconds: int) -> str:
    """Format time as SRT timestamp: HH:MM:SS,mmm"""
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"

def convert_to_srt(input_file: str, output_file: str) -> None:
    """Convert merged transcript to SRT format."""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    entries = []

    i = 0
    while i < len(lines):
        # Check if current line is a timestamp
        if re.match(r'^\d+:\d{2}$', lines[i]):
            entries.append( lines[i:i+2] )
            i += 2
        else:
            i += 1

    srt_entries = []
    for entry_number, (timestamp, subtitle_text) in enumerate(entries[:-1], start=1):
        curr_min, curr_sec = parse_timestamp(timestamp)

        next_timestamp, next_transcript = entries[entry_number]
        next_min, next_sec = parse_timestamp(next_timestamp)

        # Format SRT entry
        start_time = format_srt_time(curr_min, curr_sec)
        end_time = format_srt_time(next_min, next_sec)

        srt_entry = f"{entry_number}\n{start_time} --> {end_time}\n{subtitle_text.strip()}\n"
        srt_entries.append(srt_entry)

    # last one
    timestamp, subtitle_text = entries[-1]
    curr_min, curr_sec = parse_timestamp(timestamp)
    next_min, next_sec = curr_min, curr_sec + 3
    start_time = format_srt_time(curr_min, curr_sec)
    end_time = format_srt_time(next_min, next_sec)
    srt_entry = f"{entry_number}\n{start_time} --> {end_time}\n{subtitle_text.strip()}\n"
    srt_entries.append(srt_entry)


    # Write SRT file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_entries))

def main():
    """Main function to convert transcript to SRT."""

    input_file = "asset/transcript_ko.txt"
    output_file = Path(input_file).with_suffix(".srt")

    try:
        print("Converting merged transcript to SRT format...")
        convert_to_srt(input_file, output_file)

        print(f"✅ Successfully converted to SRT format!")
        print(f"📄 Output saved to: {output_file}")

        # Show file stats
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            entry_count = content.count('\n\n') + 1

        print(f"📊 Generated {entry_count} subtitle entries")

        # Show preview of first few entries
        lines = content.split('\n')[:15]
        print("\n📋 Preview (first entry):")
        print("-" * 50)
        for line in lines:
            print(line)

        if len(content.split('\n')) > 15:
            print("...")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise
        return 1

    return 0

if __name__ == "__main__":
    exit(main())