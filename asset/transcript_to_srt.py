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

    srt_entries = []
    entry_number = 1

    i = 0
    while i < len(lines):
        # Check if current line is a timestamp
        if re.match(r'^\d+:\d{2}$', lines[i]):
            timestamp = lines[i]

            # Get English and Korean text (next 2 lines)
            english_text = lines[i + 1] if i + 1 < len(lines) else ""
            korean_text = lines[i + 2] if i + 2 < len(lines) else ""

            # Skip entries with placeholder text
            if "[English text not available]" in english_text or "[Korean text not available]" in korean_text:
                i += 3
                continue

            # Parse current timestamp
            curr_min, curr_sec = parse_timestamp(timestamp)

            # Find next valid timestamp for end time
            next_min, next_sec = curr_min, curr_sec + 3  # Default 3 second duration

            # Look ahead for next timestamp
            j = i + 3
            while j < len(lines):
                if re.match(r'^\d+:\d{2}$', lines[j]):
                    # Check if this entry has valid content
                    has_valid_content = False
                    if j + 2 < len(lines):
                        next_english = lines[j + 1]
                        next_korean = lines[j + 2]
                        if ("[English text not available]" not in next_english and
                            "[Korean text not available]" not in next_korean):
                            has_valid_content = True

                    if has_valid_content:
                        next_min, next_sec = parse_timestamp(lines[j])
                        break
                j += 1

            # Format SRT entry
            start_time = format_srt_time(curr_min, curr_sec)
            end_time = format_srt_time(next_min, next_sec)

            # Combine English and Korean text
            subtitle_text = f"{english_text}\n{korean_text}"

            srt_entry = f"{entry_number}\n{start_time} --> {end_time}\n{subtitle_text}\n"
            srt_entries.append(srt_entry)

            entry_number += 1
            i += 3
        else:
            i += 1

    # Write SRT file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_entries))

def main():
    """Main function to convert transcript to SRT."""

    input_file = "asset/transcript_merged.txt"
    output_file = "asset/transcript.srt"

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
        return 1

    return 0

if __name__ == "__main__":
    exit(main())