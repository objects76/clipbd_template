
def add_linenumber(text):
    lines = text.split('\n')
    numbered_lines = [f"Line={i}. {line}" for i, line in enumerate(lines.split('\n'),start=1)]
    return '\n'.join(numbered_lines)

def get_QandA(cb_text:str):
    if len(cb_text) > 10:
        # text = '"'+text.replace("\n", "\\n")+'"'
        lines = [f"L{i}. {txt}".strip() for i, txt in enumerate(cb_text.split('\n'),start=1)]
        lines = '\n'.join(lines)
        return lines

    raise ValueError("No valid clipboard data for youtube.")


if __name__ == "__main__":
    str1 = "aa\nbb\ncc"
    str2 = add_linenumber(str1)
    print(str2)