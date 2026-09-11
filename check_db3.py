import sqlite3
import codecs

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT slot_code FROM bracket_slots WHERE slot_code LIKE '%B%' LIMIT 10")
slots = c.fetchall()

with codecs.open('db_dump2.txt', 'w', 'utf-8') as f:
    for s in slots:
        f.write(str(s[0]) + '\n')

conn.close()
