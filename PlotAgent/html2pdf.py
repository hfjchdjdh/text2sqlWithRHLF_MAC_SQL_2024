import re

content = "```pathG:/python_project/RapStarAgent/data_preview/summary.csv```"


def _parse_code(content):
    pattern = r"```path(.*)```"
    match = re.search(pattern, content, re.DOTALL)
    code_text = match.group(1) if match else content
    return code_text

print(_parse_code(content))

