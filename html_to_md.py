
import subprocess
import requests
import os

jjkim_key = os.getenv("JINA_API_KEY_JJKIM")
obj76_key = os.getenv("JINA_API_KEY_OBJ76")


def html_to_markdown(target_url: str):
    subprocess.run(["notify-send", "running", "html to markdown"], check=False)
    request_url = f"https://r.jina.ai/{target_url}"

    last_exception = None

    for i, key in enumerate([jjkim_key, obj76_key]):
        try:
            response = requests.get(
                request_url,
                headers={"Authorization": f"Bearer {key}"}
                )
            return response.text
        except Exception as e:
            last_exception = e
            continue
    assert  last_exception
    raise last_exception

