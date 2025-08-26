

def get_prompt(text:str):
    if len(text) > 10:
        return { "source_prompt": text }

    raise ValueError("No valid clipboard data for youtube.")
