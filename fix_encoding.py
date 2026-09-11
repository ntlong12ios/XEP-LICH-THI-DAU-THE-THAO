import codecs

def my_replace(exc):
    if isinstance(exc, UnicodeEncodeError):
        res = bytes([ord(c) for c in exc.object[exc.start:exc.end]])
        return (res, exc.end)
    raise TypeError("can't handle %s" % exc.__name__)
codecs.register_error('my_replace', my_replace)

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'rb') as f:
    data = f.read()
text = data.decode('utf-8-sig')
original_bytes = text.encode('windows-1252', errors='my_replace')

# The text contains tennis emojis 🎾 replacing ping pong 🏓.
# The tennis emoji in utf-8 was mapped to cp1252. Wait.
# If I just encode back, I'll get the raw bytes of the mangled tennis emoji?
# Let's decode it.
try:
    original_string = original_bytes.decode('utf-8')
    with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
        f.write(original_string)
    print("SUCCESS")
except Exception as e:
    print("Decode Error:", e)
