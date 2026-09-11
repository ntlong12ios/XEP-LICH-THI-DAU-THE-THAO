import codecs

def my_replace(exc):
    if isinstance(exc, UnicodeEncodeError):
        res = bytes([ord(c) for c in exc.object[exc.start:exc.end] if ord(c) < 256])
        return (res, exc.end)
    raise TypeError("can't handle %s" % exc.__name__)
codecs.register_error('my_replace', my_replace)

file_path = r'backend\main.py'
with open(file_path, 'rb') as f:
    data = f.read()

text = data.decode('utf-8-sig')
original_bytes = text.encode('windows-1252', errors='my_replace')

try:
    original_string = original_bytes.decode('utf-8')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(original_string)
    print("FIX ENCODING SUCCESS")
except Exception as e:
    print("Decode Error:", e)
