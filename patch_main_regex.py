import codecs
import re

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

# Replace any garbled Sân bóng and Sân
text = re.sub(r'f"S\w*?n b\w*?ng \{col_idx - 11\}"', 'f"S\\u00e2n b\\u00f3ng {col_idx - 11}"', text)
text = re.sub(r'f"S\w*?n \{col_idx - 4\}"', 'f"S\\u00e2n {col_idx - 4}"', text)

# Replace any garbled Tranh h?ng 3
text = re.sub(r'match_code == "Tranh h\w*?ng 3"', 'match_code == "Tranh h\\u1ea1ng 3"', text)
text = re.sub(r'match_code = "Tranh h\w*?ng 3"', 'match_code = "Tranh h\\u1ea1ng 3"', text)

# Replace N.N?
text = re.sub(r'"N\.N\w*?" in match_code', '"N.N\\u1eef" in match_code', text)

# Replace N? TK/BK/CK/3-4
text = re.sub(r'"N\w*? TK" in match_code', '"N\\u1eef TK" in match_code', text)
text = re.sub(r'"N\w*? BK" in match_code', '"N\\u1eef BK" in match_code', text)
text = re.sub(r'"N\w*? CK" in match_code', '"N\\u1eef CK" in match_code', text)
text = re.sub(r'"N\w*? 3-4" in match_code', '"N\\u1eef 3-4" in match_code', text)

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)

print("Regex Patch applied.")
