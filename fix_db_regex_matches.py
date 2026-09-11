import sqlite3

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT id, match_code FROM matches")
matches = c.fetchall()

for row in matches:
    mid, code = row
    if code:
        import re
        new_code = code
        # Fix Bảng X
        new_code = re.sub(r'B.*?ng ([A-Z])', r'Bảng \1', new_code)
        # Fix Tứ kết
        new_code = re.sub(r'T.*? k.*?t', r'Tứ kết', new_code)
        # Fix Bán kết
        new_code = re.sub(r'B.*?n k.*?t', r'Bán kết', new_code)
        # Fix Tranh hạng 3
        new_code = re.sub(r'Tranh h.*?ng 3', r'Tranh hạng 3', new_code)
        # Fix Chung kết
        new_code = re.sub(r'Chung k.*?t', r'Chung kết', new_code)
        
        c.execute("UPDATE matches SET match_code = ? WHERE id = ?", (new_code, mid))

conn.commit()
conn.close()
print("Fixed matches with regex!")
