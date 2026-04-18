import os
import re
from pathlib import Path

def check_math_balance(text):
    # Ignore $$ blocks
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    # Find all $ on each line
    lines = text.split('\n')
    unbalanced = []
    for i, line in enumerate(lines):
        # Count non-escaped $
        dollars = re.findall(r'(?<!\\)\$', line)
        if len(dollars) % 2 != 0:
            unbalanced.append((i + 1, line.strip()))
    return unbalanced

root = Path('.')
for folder in ['MML', 'Note']:
    for f in (root / folder).rglob('*.md'):
        content = f.read_text(encoding='utf-8')
        errors = check_math_balance(content)
        if errors:
            print(f"File: {f}")
            for line_no, content in errors:
                print(f"  Line {line_no}: {content}")
