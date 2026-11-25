with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def get_customer_user' in l:
        print(''.join(lines[i:i+20]))
        break
