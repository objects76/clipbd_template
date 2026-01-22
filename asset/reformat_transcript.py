#!/usr/bin/env python3
"""
Convert multi-line transcript to single line format with timestamps.
"""


def convert_transcript(input_file, output_file):
    """Convert transcript from multi-line to single line format."""

    with open(input_file, encoding="utf-8") as f:
        lines = f.readlines()

    converted_lines = []
    current_text = []
    current_timestamp = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line starts with spaces and contains → and : (timestamp line)
        if (
            "→" in line
            and ":" in line
            and line.lstrip()
            .replace("→", "")
            .replace(":", "")
            .replace(".", "")
            .isdigit()
        ):
            # If we have accumulated text, write it out
            if current_timestamp and current_text:
                text = " ".join(current_text)
                converted_lines.append(f"{current_timestamp}")
                converted_lines.append(text)
                current_text = []

            # Extract timestamp (everything after →)
            timestamp_part = line.split("→")[1].strip()
            if timestamp_part:
                current_timestamp = f"({timestamp_part})"
        else:
            # Check if line looks like just a timestamp (like "0:05")
            stripped = line.strip()
            if (
                ":" in stripped
                and len(stripped) <= 6
                and stripped.replace(":", "").isdigit()
            ):
                # If we have accumulated text, write it out
                if current_timestamp and current_text:
                    text = " ".join(current_text)
                    converted_lines.append(f"{current_timestamp}")
                    converted_lines.append(text)
                    current_text = []
                current_timestamp = f"({stripped})"
            # This is content text, accumulate it
            elif line:
                current_text.append(line)

    # Handle the last accumulated text
    if current_timestamp and current_text:
        text = " ".join(current_text)
        converted_lines.append(f"{current_timestamp}")
        converted_lines.append(text)

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in converted_lines:
            f.write(line + "\n")

    print(f"Conversion complete! Output saved to: {output_file}")
    print(f"Converted {len(converted_lines) // 2} segments")


if __name__ == "__main__":
    input_file = "asset/transcript_ko.txt"
    output_file = "asset/transcript_ko2.txt"

    convert_transcript(input_file, output_file)
