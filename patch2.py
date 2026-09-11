import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'elif "Nam TK" in match_code' in line:
        if 'cat_id = 3' in lines[i+1]:
            lines[i+1] = lines[i+1].replace('cat_id = 3', 'cat_id = 2')
    if 'TK" in match_code or' in line and 'BK" in match_code' in line and 'CK" in match_code' in line:
        if 'cat_id = 5' in lines[i+1]:
            lines[i+1] = lines[i+1].replace('cat_id = 5', 'cat_id = 4')

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.writelines(lines)
