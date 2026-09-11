import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'if "N.N\\u1eef" in match_code:' in line:
        lines[i+2] = '                elif "Nam TK" in match_code or "Nam BK" in match_code or "Nam CK" in match_code or "Nam 3-4" in match_code:\n'
        lines[i+3] = '                    cat_id = 2\n'
        lines[i+4] = '                elif "N\\u1eef TK" in match_code or "N\\u1eef BK" in match_code or "N\\u1eef CK" in match_code or "N\\u1eef 3-4" in match_code:\n'
        lines[i+5] = '                    cat_id = 4\n'

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.writelines(lines)
