with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'def get_customer_user.*?return.*?\n', text, re.DOTALL)
if m:
    print(m.group(0))
else:
    print("Not found")
