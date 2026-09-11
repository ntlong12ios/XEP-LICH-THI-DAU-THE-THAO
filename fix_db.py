import sqlite3

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

# Fix bracket_slots
c.execute("UPDATE bracket_slots SET slot_code = REPLACE(slot_code, 'Báº£ng', 'Bảng')")
c.execute("UPDATE bracket_slots SET slot_code = REPLACE(slot_code, 'Ä á»™i', 'Đội')")
c.execute("UPDATE bracket_slots SET slot_code = REPLACE(slot_code, 'Tráº­n', 'Trận')")
c.execute("UPDATE bracket_slots SET slot_code = REPLACE(slot_code, 'BÄ  Nam', 'BĐ Nam')")

c.execute("UPDATE bracket_slots SET label = REPLACE(label, 'Báº£ng', 'Bảng')")
c.execute("UPDATE bracket_slots SET label = REPLACE(label, 'Ä á»™i', 'Đội')")
c.execute("UPDATE bracket_slots SET label = REPLACE(label, 'Tráº­n', 'Trận')")

# Check matches if there's any corruption
c.execute("UPDATE matches SET match_code = REPLACE(match_code, 'Báº£ng', 'Bảng')")
c.execute("UPDATE matches SET match_code = REPLACE(match_code, 'Ä á»™i', 'Đội')")
c.execute("UPDATE matches SET match_code = REPLACE(match_code, 'Tráº­n', 'Trận')")
c.execute("UPDATE matches SET match_code = REPLACE(match_code, 'TÃ¡Â»Â©', 'Tứ')")
c.execute("UPDATE matches SET match_code = REPLACE(match_code, 'BÃ¡ÂºÂ¡n', 'Bán')")

conn.commit()
conn.close()
print("Database fixed!")
