with open('myproject/templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('id="food"')
print(text[idx+1200:idx+2500])
