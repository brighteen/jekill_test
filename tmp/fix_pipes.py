import sys
import re

def replace_pipes_and_wrap(match):
    # Replace pipes with \mid
    content = match.group(0).replace('|', r'\mid ')
    # If it's single dollar math, convert to double dollar
    if content.startswith('$') and not content.startswith('$$'):
        return f'${content}$'
    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inline math: $ ... $ (specifically single dollars)
    # Using negative lookbehind/ahead to avoid matching parts of $$
    content = re.sub(r'(?<!\$)\$[^$\n]+\$(?!\$)', replace_pipes_and_wrap, content)
    
    # Block math: $$ ... $$
    content = re.sub(r'\$\$.*?\$\$', replace_pipes_and_wrap, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        print(f"Processing {file_path}...")
        process_file(file_path)
