with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def login' in l or 'def user_login' in l or 'role_redirect' in l:
        print(''.join(lines[i:i+40]))
        break
