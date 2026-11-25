with open('myproject/templates/login.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of login.html:", len(text))
print("First 500 chars:\n", text[:500])
