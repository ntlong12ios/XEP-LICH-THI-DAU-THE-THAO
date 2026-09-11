import sqlite3
import codecs

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT slot_code FROM bracket_slots LIMIT 20")
slots = c.fetchall()

with codecs.open('db_dump.txt', 'w', 'utf-8') as f:
    for s in slots:
        f.write(str(s[0]) + '\n')

conn.close()
