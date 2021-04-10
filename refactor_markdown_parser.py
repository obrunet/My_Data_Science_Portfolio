""""
About this exercise
Refactor a Markdown parser
"""


import re


def parse(markdown):
    res = ''
    in_list = False

    for line in markdown.split('\n'):
        # Headers
        line = parse_headers(line)
        # bold
        line = parse_bold(line)
        # italic
        line = parse_italic(line)

        m = re.match(r'\* (.*)', line)
        if m:
            line = f"<li>{m.group(1)}</li>"
            if not in_list:
                in_list = True
                line = f"<ul>{line}"

        m = re.match('<h|<ul|<p|<li', line)
        if not m:
            line = f"<p>{line}</p>"
            if in_list:
                in_list = False
                line = f"</ul>{line}"

        res += line

    # close list if there are no more lines left that can close it and it's still open
    if in_list:
        res += '</ul>'
    return res


def parse_headers(line):
    # H6
    if re.match('###### (.*)', line):
        return f"<h6>{line[7:]}</h6>"
    # H2
    if re.match('## (.*)', line):
        return f"<h2>{line[3:]}</h2>"
    # H1
    if re.match('# (.*)', line):
        return f"<h1>{line[2:]}</h1>"
    return line


def parse_bold(line):
    m = re.match('(.*)__(.*)__(.*)', line)
    if m:
        return f"{m.group(1)}<strong>{m.group(2)}</strong>{m.group(3)}"
    return line


def parse_italic(line):
    m = re.match('(.*)_(.*)_(.*)', line)
    if m:
        return f"{m.group(1)}<em>{m.group(2)}</em>{m.group(3)}"
    return line