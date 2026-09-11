with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r'\n', '\n')

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'r', encoding='utf-8') as f:
    text2 = f.read()
text2 = text2.replace(r'\"', '"').replace('`"http://`', '`http://')
with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'w', encoding='utf-8') as f:
    f.write(text2)

print("Fixed newlines and quotes!")
