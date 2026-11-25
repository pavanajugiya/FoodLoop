with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'def customer_\w+', text)]
for m in matches:
    print(text[m:m+200])
    print("="*40)
