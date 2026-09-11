import re
import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

# Make absolutely sure we use pure unicode escapes to bypass Windows Python encoding reading issues
text = text.replace('f"Bảng {g_name} - Đội {pos}"', 'f"B\\u1ea3ng {g_name} - \\u0110\\u1ed9i {pos}"')
text = text.replace('f"Bảng {i+1}"', 'f"B\\u1ea3ng {i+1}"')
text = text.replace('label=f"Bảng {g_name}"', 'label=f"B\\u1ea3ng {g_name}"')

# Also fix the previous broken attempts if they exist
text = text.replace('f"B?ng {g_name} - D?i {pos}"', 'f"B\\u1ea3ng {g_name} - \\u0110\\u1ed9i {pos}"')
text = text.replace('f"B?ng {i+1}"', 'f"B\\u1ea3ng {i+1}"')
text = text.replace('label=f"B?ng {g_name}"', 'label=f"B\\u1ea3ng {g_name}"')

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)
    
print("Updated main.py to use safe unicode escapes!")
