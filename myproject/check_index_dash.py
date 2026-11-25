with open('myproject/templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<a[^>]*href="[^"]*dashboard[^"]*"[^>]*>.*?</a>', text, re.DOTALL)
print("Dashboard links in index.html:")
for m in matches:
    print(m.strip()[:150])
