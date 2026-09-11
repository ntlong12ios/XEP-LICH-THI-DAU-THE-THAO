import json
import urllib.request

req = urllib.request.urlopen('http://localhost:8000/categories/4/bracket_slots')
data = json.loads(req.read())
code = data[0]['slot_code']
for c in code:
    print(hex(ord(c)))
