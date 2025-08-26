from copyq import get_lastest_clipboard
def add_linenumber(text):
    lines = text.split('\n')
    numbered_lines = [f"Line={i}. {line}" for i, line in enumerate(lines.split('\n'),start=1)]
    return '\n'.join(numbered_lines)

def get_QandA():
    items = get_lastest_clipboard(n=1)
    for i, item in enumerate(items, start=1):
        if item['type'] != 'text': continue
        text = item['data'].strip()
        if len(text) > 10:
            # text = '"'+text.replace("\n", "\\n")+'"'
            text = [f"L{i}. {txt}".strip() for i, txt in enumerate(text.split('\n'),start=1)]
            text = '\n'.join(text)
            return { "context": {text}, "query": "your_question_here" }

    raise ValueError("No valid clipboard data for youtube.")


if __name__ == "__main__":
    str1 = "aa\nbb\ncc"
    str2 = add_linenumber(str1)
    print(str2)