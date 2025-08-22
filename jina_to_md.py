
import subprocess
import requests
import os

from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.config/rofi/.env"))
jjkim_key = os.getenv("JINA_API_JJKIM")
obj76_key = os.getenv("JINA_API_OBJECTS76")

#
# curl "https://r.jina.ai/https://www.example.com" \
#   -H "Accept: text/event-stream" \
#   -H "Authorization: Bearer jina_de01014707b44f2b8da84917e486c09e_y-mapgpzKFuLA9iutoemgnK1eRw" \
#   -H "X-Respond-With: readerlm-v2"


instruction = "Extract the main content from the given HTML and convert it to Markdown format."

def jina_to_md(target_url: str):
    subprocess.run(["notify-send", "running", f"jina({target_url}) to markdown"], check=False)
    request_url = f"https://r.jina.ai/{target_url}"

    last_exception = None

    for i, key in enumerate([jjkim_key, obj76_key]):
        try:
            response = requests.get(
                request_url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "X-Respond-With": "readerlm-v2",
                })
            return response.text
        except Exception as e:
            last_exception = e
            continue
    assert  last_exception
    raise last_exception

def test():
    md_text = jina_to_md("https://huggingface.co/jinaai/ReaderLM-v2")
    print(md_text)

if __name__ == '__main__':
    test()