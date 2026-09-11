import sqlite3

conn = sqlite3.connect('backend/sport_tournament.db')
c = conn.cursor()

c.execute("SELECT slot_code FROM bracket_slots LIMIT 5")
print("Slots:", c.fetchall())

c.execute("SELECT match_code FROM matches LIMIT 5")
print("Matches:", c.fetchall())

conn.close()
