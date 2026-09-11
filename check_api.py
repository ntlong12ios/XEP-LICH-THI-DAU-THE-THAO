import urllib.request, json
req = urllib.request.Request('https://xep-lich-thi-dau-the-thao-q1j5o2jh9.vercel.app/api/verify_admin', data=b'{"password":"admin@1234"}', headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as f:
        print("Success:", f.read().decode())
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
