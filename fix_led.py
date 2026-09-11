with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('axios.get(${API}/led_state)', 'axios.get(`${API}/led_state`)')

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
print("LedScreen fixed!")
