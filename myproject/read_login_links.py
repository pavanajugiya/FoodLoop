with open('myproject/templates/login.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Links in login.html:")
for a in re.findall(r'<a.*?>.*?</a>', text):
    print(a)
