import codecs

with codecs.open('src/App.tsx', 'r', 'utf-8') as f:
    text = f.read()

try:
    # Encode as cp1252 to get the original utf-8 bytes
    raw_bytes = text.encode('cp1252')
    # Decode as utf-8
    fixed_text = raw_bytes.decode('utf-8')
    
    if "Bóng đá" in fixed_text:
        with codecs.open('src/App.tsx', 'w', 'utf-8') as fw:
            fw.write(fixed_text)
        print("Fixed via cp1252!")
    else:
        print("Still didn't find Bóng đá")
except Exception as e:
    print("Error:", e)
