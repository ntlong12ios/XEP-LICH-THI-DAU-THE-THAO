import os
import re

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\{isAdmin && <button className="btn btn-secondary" onClick=\{loadAgenda\} disabled=\{genLoading\}>\s*\{genLoading \? \'⏳\' : \'📥\'\} Tải Agenda từ Excel\s*</button>\}'

new_btn = """{isAdmin && <label className="btn btn-secondary" style={{cursor: 'pointer', display: 'inline-flex', alignItems: 'center'}}>
          {genLoading ? '⏳' : '📥'} Tải Agenda từ Excel
          <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleAgendaUpload} disabled={genLoading} />
        </label>}"""

if re.search(pattern, content):
    content = re.sub(pattern, new_btn, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched App.tsx loadAgenda button")
else:
    print("Pattern not found!")
