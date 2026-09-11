import sqlite3
import re

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT id, slot_code, label FROM bracket_slots")
slots = c.fetchall()

for row in slots:
    sid, code, label = row
    if code:
        new_code = re.sub(r'B.*?ng ([A-Z]) - .*?(\d+)', 'B\u1ea3ng \\1 - \u0110\u1ed9i \\2', code)
        # Also fix plain "Bảng X" if it's corrupted in label
        new_label = label
        if label:
            new_label = re.sub(r'B.*?ng ([A-Z])', 'B\u1ea3ng \\1', label)
        c.execute("UPDATE bracket_slots SET slot_code = ?, label = ? WHERE id = ?", (new_code, new_label, sid))

conn.commit()
conn.close()
print("Fixed slots with pure unicode escapes!")
