import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

try:
    # First, let's just replace the known corrupted strings manually 
    # to be safe and not break any actual code!
    replacements = {
        "Báº£ng": "Bảng",
        "Ä á»™i": "Đội",
        "BÃ³ng Ä‘Ã¡": "Bóng đá",
        "Tráº­n": "Trận",
        "BÄ  Nam ": "BĐ Nam "
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
        
    with codecs.open('backend/main.py', 'w', 'utf-8') as fw:
        fw.write(text)
    print("Replaced corrupted strings in main.py!")
except Exception as e:
    print("Error:", e)
