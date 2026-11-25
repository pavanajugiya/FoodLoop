with open('myproject/templates/dashboard-customer.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
forms = re.findall(r'<form.*?>', text)
modals = re.findall(r'<div class="modal.*?>', text)
scripts = re.findall(r'<script.*?>.*?</script>', text, re.DOTALL)

print("Forms found:", len(forms))
for form in forms:
    print(form)

print("\nModals found:", len(modals))
for m in re.findall(r'<div class="modal-overlay".*?>', text):
    print(m)

print("\nScripts summary:")
if scripts:
    s = scripts[0]
    fns = re.findall(r'function \w+\(.*?\)', s)
    for fn in fns:
        print("  ", fn)
