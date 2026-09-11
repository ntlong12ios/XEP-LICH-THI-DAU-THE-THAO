import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

upload_agenda_fn = """
  const handleAgendaUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    setGenLoading(true);
    axios.post(`${API}/load_agenda`, formData)
      .then(r => { 
          alert(r.data.message); 
          onRefresh(); 
      })
      .catch(err => alert('Lỗi tải Agenda: ' + (err.response?.data?.detail || err.message)))
      .finally(() => setGenLoading(false));
    e.target.value = '';
  }
"""

# Replace `loadAgenda` function completely
old_load_agenda = """  const loadAgenda = () => {

    setGenLoading(true)

    axios.post(`${API}/load_agenda`)

      .then(r => {

        alert(r.data.message)

        onRefresh()

      })

      .catch(e => {

        const detail = e.response?.data?.detail || 'Lỗi tải Agenda!'

        alert(detail)

      })

      .finally(() => setGenLoading(false))

  }"""

import re
# Regex to remove the old loadAgenda function, handling varying whitespaces
content = re.sub(r'const loadAgenda = \(\) => \{.*?finally\(\(\) => setGenLoading\(false\)\)\s*\}', upload_agenda_fn.strip(), content, flags=re.DOTALL)

# Replace the button
old_btn = """<button className="btn btn-secondary" onClick={loadAgenda} disabled={genLoading}>
          {genLoading ? '⏳' : '📥'} Tải Agenda từ Excel
        </button>"""
new_btn = """<label className="btn btn-secondary" style={{cursor: 'pointer', display: 'inline-flex', alignItems: 'center'}}>
          {genLoading ? '⏳' : '📥'} Tải Agenda từ Excel
          <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleAgendaUpload} disabled={genLoading} />
        </label>"""
content = content.replace(old_btn, new_btn)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched frontend load_agenda")
