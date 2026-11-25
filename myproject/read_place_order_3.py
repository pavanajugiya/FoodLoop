with open('myproject/home/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def customer_place_order' in l:
        print(''.join(lines[i+70:i+110]))
        break
