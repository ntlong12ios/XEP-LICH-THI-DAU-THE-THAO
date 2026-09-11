import sqlite3
import re

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT id, slot_code, label FROM bracket_slots")
slots = c.fetchall()

for row in slots:
    sid, code, label = row
    if code and '-' in code and 'ng ' in code:
        # Match "Bảng X - something Y"
        new_code = re.sub(r'B.*?ng ([A-Z]) - .*?(\d+)', r'Bảng \1 - Đội \2', code)
        c.execute("UPDATE bracket_slots SET slot_code = ? WHERE id = ?", (new_code, sid))

conn.commit()
conn.close()
print("Fixed category 4 and others!")
