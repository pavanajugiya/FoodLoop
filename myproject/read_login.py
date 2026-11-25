with open('myproject/templates/login.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<button.*?</button>|<a.*?</a>', text, re.DOTALL)
for m in matches:
    if 'customer' in m.lower() or 'demo' in m.lower():
        print(m.strip())
