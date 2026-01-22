#!/usr/bin/env python3
"""
Merge English and Korean transcripts into a unified format.
Format: timestamp -> English text -> Korean text
"""

import re
from pathlib import Path


def parse_transcript_section(section: str) -> dict[str, str]:
    """Extract transcript entries from a section between markers."""

    # Parse entries: timestamp -> text
    entries = {}
    lines = section.strip().split("\n")

    current_timestamp = None
    current_text_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line is a timestamp (format: "0:00" or "0:17")
        timestamp_match = re.match(r"^\d+:\d{2}$", line)

        if timestamp_match:
            # Save previous entry if exists
            if current_timestamp and current_text_lines:
                entries[current_timestamp] = " ".join(current_text_lines)

            # Start new entry
            current_timestamp = line
            current_text_lines = []
        # This is text content
        elif current_timestamp:
            current_text_lines.append(line)

    # Save the last entry
    if current_timestamp and current_text_lines:
        entries[current_timestamp] = " ".join(current_text_lines)

    return entries


def merge_transcripts(english_path: str, korean_path: str) -> str:
    """Merge English and Korean transcripts from the file."""

    # Parse both sections
    eng = Path(english_path).read_text(encoding="utf-8")
    ko = Path(korean_path).read_text(encoding="utf-8")
    english_entries = parse_transcript_section(eng)
    korean_entries = parse_transcript_section(ko)

    # Get all unique timestamps and sort them
    all_timestamps = set(english_entries.keys()) | set(korean_entries.keys())

    # Convert timestamps to sortable format for proper ordering
    def timestamp_to_seconds(timestamp: str) -> float:
        parts = timestamp.split(":")
        return int(parts[0]) * 60 + int(parts[1])

    sorted_timestamps = sorted(all_timestamps, key=timestamp_to_seconds)

    # Build merged transcript
    merged_lines = []

    for timestamp in sorted_timestamps:
        merged_lines.append(timestamp)

        # Add English text
        english_text = english_entries.get(timestamp, "[English text not available]")
        merged_lines.append(english_text)

        # Add Korean text
        korean_text = korean_entries.get(timestamp, "[Korean text not available]")
        merged_lines.append(korean_text)

        # Add empty line for readability
        merged_lines.append("")

    return "\n".join(merged_lines)


def main():
    """Main function to merge transcripts."""

    output_file = "asset/transcript_merged.txt"

    try:
        print("Parsing transcripts...")
        merged_content = merge_transcripts(
            "asset/transcript_en.txt", "asset/transcript_ko.txt"
        )

        # Write merged transcript
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(merged_content)

        print("✅ Successfully merged transcripts!")
        print(f"📄 Output saved to: {output_file}")

        # Show preview of first few entries
        lines = merged_content.split("\n")[:20]
        print("\n📋 Preview (first few entries):")
        print("-" * 50)
        for line in lines:
            print(line)

        if len(merged_content.split("\n")) > 20:
            print("...")
            print(f"({len(merged_content.split('\n'))} total lines)")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
