
import subprocess
import requests


def html_to_markdown(target_url: str):
    subprocess.run(["notify-send", "running", "html to markdown"], check=False)
    request_url = f"https://r.jina.ai/{target_url}"

    last_exception = None
    jjkim_key = "jina_7486fd840bda4ea9b428afbaab1d62706gksDo-ypWXbUO7QHwzukzeBujN_"
    obj76_key = "jina_de01014707b44f2b8da84917e486c09e_y-mapgpzKFuLA9iutoemgnK1eRw"
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

