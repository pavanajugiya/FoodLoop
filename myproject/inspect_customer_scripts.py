with open('myproject/templates/dashboard-customer.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>.*?</script>', text, re.DOTALL)
print("Scripts count:", len(scripts))
for i, s in enumerate(scripts):
    print(f"\n--- Script {i} (len: {len(s)}) ---")
    fns = re.findall(r'function (\w+)\s*\(', s)
    print("Functions:", fns)
