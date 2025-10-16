
import subprocess
import time
from typing import Callable
from openai import OpenAI
import anthropic
import base64
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def openai_inference(
    prompt: str,
    instructions: str|None = None,
    image_path: str|None = None,
    *,
    reasoning_effort: str|None = None,  # "low" | "medium" | "high"
    model: str = "gpt-5",
    print_stream: Callable|None = None,
) -> str:
    """Perform LLM inference using OpenAI Responses API with optional streaming.

    Args:
        prompt: The user input.
        instructions: High-level system/developer guidance.
        reasoning_effort: One of {"low","medium","high"} for reasoning models.
        model: Model name, defaults to "gpt-5-mini".
        print_stream: Callback to receive streaming text chunks; if None, no streaming.

    Returns:
        The full assistant text.
    """
    load_dotenv()
    client = OpenAI()

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    user_content = [{ "type": "input_text", "text": prompt.strip() }]

    if image_path and Path(image_path).is_file():
        user_content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{encode_image(image_path)}",
        })

    messages:list[dict] = [{"role": "developer", "content": instructions.strip()}] if instructions else []
    messages.append({"role": "user", "content": user_content})


    params = {
        "model": model,
        "input": messages,
    }
    if reasoning_effort:
        params["reasoning"] = {"effort": reasoning_effort}

    # Check if we need to force streaming for large requests
    input_size = len(str(messages))
    force_streaming = input_size > 15000  # Force streaming for large inputs
    print('input length: ', input_size, force_streaming)

    # Streaming path
    if print_stream is not None or force_streaming:
        full_text: list[str] = []
        with client.responses.stream(**params) as stream:
            print_stream = print_stream or (lambda x: print(f'stream: {len(x)}...', end='\r', flush=True))
            for event in stream:
                if event.type == "response.output_text.delta":
                    piece = event.delta or ""
                    print_stream(piece)
                    full_text.append(piece)
                elif event.type == "response.error":
                    # Surface errors immediately
                    raise RuntimeError(str(event.error))
            # Optional: retrieve the final consolidated response object
            _final = stream.get_final_response()
        return "".join(full_text)

    # Non-streaming path
    resp = client.responses.create(**params)
    return resp.output_text

# https://docs.anthropic.com/en/api/client-sdks
# "claude-3-7-sonnet-latest"  # alias
# "claude-sonnet-4-0"  # alias
# "claude-opus-4-0"  # alias
# "claude-opus-4-1"  # alias

def anthropic_inference(
    prompt: str,
    instructions: str|None = None,
    image_path: str|None = None,
    *,
    model: str = "claude-sonnet-4-0",
    print_stream: Callable|None = None,
) -> str:
    """Perform LLM inference using Anthropic API with optional streaming.

    Args:
        prompt: The user input.
        instructions: High-level system/developer guidance.
        image_path: Path to image file for vision capabilities.
        model: Model name, defaults to "claude-3-5-sonnet-latest".
        print_stream: Callback to receive streaming text chunks; if None, no streaming.

    Returns:
        The full assistant text.
    """
    load_dotenv()
    client = anthropic.Anthropic()

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Build messages
    messages = []

    # User message content
    user_content = [{"type": "text", "text": prompt.strip()}]

    if image_path and Path(image_path).is_file():
        # Determine image media type
        image_ext = Path(image_path).suffix.lower()
        media_type = "image/jpeg"  # default
        if image_ext in ['.png', '.gif', '.webp']:
            media_type = f"image/{image_ext[1:]}"

        user_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": encode_image(image_path)
            }
        })

    messages.append({"role": "user", "content": user_content})

    params = {
        "model": model,
        "max_tokens": 32*1024,
        "messages": messages,
    }

    if instructions:
        params["system"] = instructions.strip()


    # Check if we need to force streaming for large requests
    input_size = len(str(messages))
    force_streaming = input_size > 15000  # Force streaming for large inputs
    print('input length: ', input_size, force_streaming)

    # Streaming path (forced for large requests or when print_stream is provided)
    if print_stream is not None or force_streaming:
        full_text: list[str] = []
        with client.messages.stream(**params) as stream:
            print_stream = print_stream or (lambda x: print(f'stream: {len(x)}...', end='\r', flush=True))
            for text in stream.text_stream:
                print_stream(text)
                full_text.append(text)
        return "".join(full_text)

    # Non-streaming path (only for smaller requests)
    try:
        response = client.messages.create(**params)
        return response.content[0].text
    except ValueError as e:
        if "Streaming is required" in str(e):
            # Fallback to streaming if non-streaming fails
            full_text: list[str] = []
            with client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    full_text.append(text)
            return "".join(full_text)
        else:
            raise


SYSTEM_PROMPT = """
{
  "task": "translate youtube transcript into Korean",
  "instructions": [
    "Keep the original document format (timestamp, text, etc.).",
    "Translate the entire transcript fully into Korean without omitting or skipping any part."
  ],
  "final_check": "Carefully review the entire content to ensure that everything has been translated into Korean without omissions."
}
"""

def get_latest_srt():
    srt_files = Path(__file__).parent.glob("*.srt")
    srt_files = [srt_file for srt_file in srt_files if "ko" not in srt_file.name]
    return max(srt_files, key=lambda f: f.stat().st_mtime)


def main():
    srt_path = get_latest_srt()
    with open(srt_path, 'r', encoding='utf-8') as f:
        transcript = f.read()

    prompt = f"<transcript>\n{transcript}\n</transcript>"
    # result = openai_inference(prompt, SYSTEM_PROMPT, model = "gpt-5")

    result = anthropic_inference(
        prompt, SYSTEM_PROMPT,
        model = "claude-sonnet-4-0",
        # print_stream=lambda x: print(x, end='', flush=True),
    )
    with open(srt_path.with_suffix(".ko.srt"), 'w', encoding='utf-8') as f:
        f.write(result)
    print("\n\n--- Translation Complete ---")

    return 0

if __name__ == "__main__":
    exit(main())