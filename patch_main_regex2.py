import codecs
import re

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

text = re.sub(r'f"S.*?n b.*?ng \{col_idx - 11\}"', lambda m: 'f"S\\u00e2n b\\u00f3ng {col_idx - 11}"', text)
text = re.sub(r'f"S.*?n \{col_idx - 4\}"', lambda m: 'f"S\\u00e2n {col_idx - 4}"', text)

text = re.sub(r'match_code == "Tranh h.*?ng 3"', lambda m: 'match_code == "Tranh h\\u1ea1ng 3"', text)
text = re.sub(r'match_code = "Tranh h.*?ng 3"', lambda m: 'match_code = "Tranh h\\u1ea1ng 3"', text)

text = re.sub(r'"N\.N.*?" in match_code', lambda m: '"N.N\\u1eef" in match_code', text)

text = re.sub(r'"N.*? TK" in match_code', lambda m: '"N\\u1eef TK" in match_code', text)
text = re.sub(r'"N.*? BK" in match_code', lambda m: '"N\\u1eef BK" in match_code', text)
text = re.sub(r'"N.*? CK" in match_code', lambda m: '"N\\u1eef CK" in match_code', text)
text = re.sub(r'"N.*? 3-4" in match_code', lambda m: '"N\\u1eef 3-4" in match_code', text)

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)

print("Regex Patch applied.")
