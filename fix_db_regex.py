import sqlite3

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT id, slot_code, label FROM bracket_slots")
slots = c.fetchall()

for row in slots:
    sid, code, label = row
    if code:
        # It has "Ãá»™i" or whatever corrupted "Đội". Let's just fix it.
        # "Đội" might be corrupted. 
        # Since we know the format is "Bảng X - Đội Y", let's just use regex.
        import re
        new_code = re.sub(r'B.*?ng ([A-Z]) - .*?i (\d+)', r'Bảng \1 - Đội \2', code)
        # Also fix any "BĐ Nam" if it got weirdly corrupted
        new_code = re.sub(r'B.*Nam', 'BĐ Nam', new_code)
        
        new_label = label
        if label:
            new_label = re.sub(r'B.*?ng ([A-Z])', r'Bảng \1', label)
            
        c.execute("UPDATE bracket_slots SET slot_code = ?, label = ? WHERE id = ?", (new_code, new_label, sid))

conn.commit()
conn.close()
print("Fixed slots with regex!")
