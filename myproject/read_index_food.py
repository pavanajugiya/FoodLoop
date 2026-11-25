with open('myproject/templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('id="food"')
if idx != -1:
    print(text[idx:idx+1200])
else:
    print("id='food' not found")
