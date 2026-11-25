with open('myproject/templates/dashboard-customer.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(''.join(lines[190:260]))
