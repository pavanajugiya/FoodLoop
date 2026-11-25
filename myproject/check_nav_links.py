with open('myproject/templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<a.*?class="nav-link".*?>.*?</a>', text)
print("Nav links in index.html:")
for m in matches:
    print(m)
