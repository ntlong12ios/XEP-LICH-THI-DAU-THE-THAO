with open('backend/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(355, 365):
    print(repr(lines[i]))
