import requests

try:
    r = requests.post("http://localhost:8000/load_agenda")
    print(r.status_code)
    print(r.json())
except Exception as e:
    print(e)
