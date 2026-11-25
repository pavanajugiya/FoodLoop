with open('myproject/templates/login.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Form actions in login.html:")
for f in re.findall(r'<form.*?>', text):
    print(f)

print("\nButtons in login.html:")
for b in re.findall(r'<button.*?</button>', text, re.DOTALL):
    print(b.strip())
