import os

new_api_line = "const API = import.meta.env.PROD ? '/api' : `http://${window.location.hostname}:8000`"

for filename in ['App.tsx', 'LedScreen.tsx']:
    path = os.path.join(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src', filename)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip().startswith("const API ="):
                f.write(new_api_line + "\n")
            else:
                f.write(line)
print("Replaced API endpoints")
