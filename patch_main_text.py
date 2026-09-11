import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

# Fix court strings and category names
text = text.replace('f"Sân bóng {col_idx - 11}"', 'f"S\\u00e2n b\\u00f3ng {col_idx - 11}"')
text = text.replace('f"Sân {col_idx - 4}"', 'f"S\\u00e2n {col_idx - 4}"')
text = text.replace('match_code == "Tranh hạng 3"', 'match_code == "Tranh h\\u1ea1ng 3"')
text = text.replace('"N.Nữ" in match_code', '"N.N\\u1eef" in match_code')
text = text.replace('"Nữ TK"', '"N\\u1eef TK"')
text = text.replace('"Nữ BK"', '"N\\u1eef BK"')
text = text.replace('"Nữ CK"', '"N\\u1eef CK"')
text = text.replace('"Nữ 3-4"', '"N\\u1eef 3-4"')

# Add support for '3-4' in match_code as Tranh h?ng 3 for football and pickleball
# Original code:
# if match_code == "Tranh 3-4":
#     match_code = "Tranh h?ng 3"
text = text.replace('if match_code == "Tranh 3-4":', 'if match_code == "Tranh 3-4" or match_code == "3-4":')
text = text.replace('match_code = "Tranh hạng 3"', 'match_code = "Tranh h\\u1ea1ng 3"')

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)
print("Patch applied.")
