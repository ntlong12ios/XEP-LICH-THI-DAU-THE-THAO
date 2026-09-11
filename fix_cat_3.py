with open('backend/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'if "N.N\\u1eef" in match_code:' in line:
        if 'cat_id = 4' in lines[i+1]:
            lines[i+1] = lines[i+1].replace('cat_id = 4', 'cat_id = 3')

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
