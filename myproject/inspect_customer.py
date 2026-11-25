with open('myproject/templates/dashboard-customer.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="sec-' in l or 'showSection' in l or 'class="nav-item' in l or '<nav' in l or '<header' in l:
        print(f"{i+1}: {l.strip()}")
