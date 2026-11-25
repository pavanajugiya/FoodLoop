with open('myproject/templates/login.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'role' in l.lower() or 'quick' in l.lower() or 'demo' in l.lower() or 'customer' in l.lower():
        print(f"{i+1}: {l.strip()}")
