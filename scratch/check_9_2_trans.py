import re
from pathlib import Path

def check_total_balance(file_path):
    content = Path(file_path).read_text(encoding='utf-8')
    masked = re.sub(r'\$\$.*?\$\$', 'MASKED_BLOCK', content, flags=re.DOTALL)
    dollars = re.findall(r'(?<!\\)\$', masked)
    return len(dollars)

f = "_mml/Part II Central Machine Learning Problems/9. Linear Regression/9.2 Parameter Estimation.md"
count = check_total_balance(f)
print(f"File: {f}")
print(f"Total single dollars: {count}")
if count % 2 != 0:
    print("UNBALANCED!!")
else:
    print("Balanced.")
