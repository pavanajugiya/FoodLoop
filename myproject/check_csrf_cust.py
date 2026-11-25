with open('myproject/templates/dashboard-customer.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("csrf_token in dashboard-customer.html:", 'csrf_token' in text)
