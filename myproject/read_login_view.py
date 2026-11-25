with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def login_view' in l:
        print(''.join(lines[i:i+60]))
        break
