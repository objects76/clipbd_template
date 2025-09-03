import subprocess
import time
from typing import Callable
from openai import OpenAI
import base64
from dotenv import load_dotenv

def wait_page_loaded(needle, timeout=3):
    cmds = "xdotool search --name --class microsoft-edge"

    for i in range(timeout):
        result = subprocess.run(cmds.split(), capture_output=True, text=True, timeout=timeout)
        window_ids = [w for w in result.stdout.strip().split('\n') if w]

        for window_id in window_ids:
            print('activate: ', window_id)
            result = subprocess.run(['xdotool', 'windowactivate', window_id], capture_output=True, text=True, check=True, timeout=timeout)
            if result.returncode == 0 and not result.stderr.strip():
                print('windowactivate: ', result)

                result = subprocess.run(['xdotool', 'getwindowname', window_id], capture_output=True, text=True, check=True, timeout=timeout)
                if result.returncode == 0:
                    title = result.stdout.strip()
                    print('getwindowname: ', title)
                    if needle.lower() in title.lower():
                        print('page loaded: ', title)
                        return True
        time.sleep(1)
    return False


def run_web_llm(profile: str, url: str, wait_title:str="chatgpt") -> None:
    """Launch browser with sanitized inputs.

    Args:
        user (str): Browser profile directory name
        url (str): URL to open
    """
    BROWSER = "microsoft-edge-stable"

    print(profile, url, wait_title)

    args = [
        BROWSER,
        f'--profile-directory={profile}',
        "--new-tab",
        url
    ]
    print(args)

    subprocess.Popen(args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True)

    wait_page_loaded(wait_title, 3)
    time.sleep(1)


# Remove None values recursively from messages
def remove_none_recursive(obj):
    if isinstance(obj, dict):
        return {k: remove_none_recursive(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_recursive(item) for item in obj if item is not None]
    else:
        return obj

def openai_inference(
    prompt: str,
    instructions: str|None = None,
    image_path: str|None = None,
    reasoning_effort: str|None = None,  # "low" | "medium" | "high"
    model: str = "gpt-5-mini",
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

    messages:list[dict|None] = [
        {"role": "developer", "content": instructions} if instructions else None,
        {"role": "user", "content": [
            { "type": "input_text", "text": prompt },
            { "type": "input_image", "image_url": f"data:image/jpeg;base64,{encode_image(image_path)}", } if image_path else None,
        ]}
    ]

    messages = remove_none_recursive(messages) # type: ignore

    params = {
        "model": model,
        "input": messages,
    }
    if reasoning_effort:
        params["reasoning"] = {"effort": reasoning_effort}


    # Streaming path
    if print_stream is not None:
        full_text: list[str] = []
        with client.responses.stream(**params) as stream:
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

def split_prompt(prompt: str, sep:str) -> list[str]:
    parts = prompt.split(sep)
    return [part.strip() for part in parts if part.strip()]



def main():
    from pathlib import Path

    # Check if prompt file exists
    prompt_file = Path("asset/prompt.txt")


    # Process file with streaming
    prompt = prompt_file.read_text()
    prompts = split_prompt(prompt, sep='## Content:')

    print("Processing prompt with streaming...\n")
    print("=" * 60)

    # Use streaming to show real-time generation
    def print_stream(text_chunk):
        # Simple print function for streaming text
        print(text_chunk, end='', flush=True)

    result = openai_inference(
        prompts[1],  # Main input/prompt
        instructions=prompts[0],  # Instructions (like system prompt)
        reasoning_effort="medium",  # Not used but kept for compatibility
        print_stream=print_stream  # Show output as it generates
    )

    print("\n" + "=" * 60)
    print(f'\nResult length: {len(result)} characters')

    # Save the complete result
    Path("asset/result.md").write_text(result)
    print("Result saved to asset/result.md")


def webllm_test():
    from config import Config
    Config("asset/template2.yaml")
    print(Config.browser_profile, Config.webai, Config.webai_title, 'end', sep='!\n')


if __name__ == "__main__":
    # main()
    webllm_test()
