import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add handleFileUpload near handleInitialReload
upload_fn = """
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!window.confirm('Cập nhật lại từ file Excel sẽ ghi đè toàn bộ danh sách hiện tại. Bạn có chắc chắn không?')) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    axios.post(`${API}/upload_excel`, formData)
      .then(r => { show(r.data.message); fetchData(); })
      .catch(err => show('Lỗi tải file: ' + (err.response?.data?.detail || err.message), 'error'))
      .finally(() => setLoading(false));
    // Reset input
    e.target.value = '';
  }
"""

# Find where to inject
content = content.replace('const handleInitialReload = () => {', upload_fn + '\n  const handleInitialReload = () => {')

# Replace the empty state button
old_btn_1 = """<button className="btn btn-primary" onClick={handleInitialReload} disabled={loading}>
                   {loading ? "⏳ Đang xử lý..." : "🔄 Cập nhật dữ liệu từ Excel"}
                 </button>"""
new_btn_1 = """<label className="btn btn-primary" style={{cursor: 'pointer', display: 'inline-block'}}>
                   {loading ? "⏳ Đang xử lý..." : "🔄 Tải lên file Excel DATA"}
                   <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleFileUpload} disabled={loading} />
                 </label>"""
content = content.replace(old_btn_1, new_btn_1)

# Replace the update button in the active panel (around line 573, which is handleReload)
# Let's just find the button text and replace it with a label
old_btn_2 = """<button className="btn btn-secondary" onClick={handleReload} disabled={loading}>
            {loading ? '⏳ Đang xử lý...' : '🔄 Cập nhật lại từ file Excel'}
          </button>"""
new_btn_2 = """<label className="btn btn-secondary" style={{cursor: 'pointer', display: 'inline-flex', alignItems: 'center'}}>
            {loading ? '⏳ Đang xử lý...' : '🔄 Tải lên file Excel DATA'}
            <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleFileUpload} disabled={loading} />
          </label>"""
content = content.replace(old_btn_2, new_btn_2)

# Also replace handleReload usages where they pass it to DrawScreen or TeamsScreen if any?
# Wait, handleReload is used inside TeamsScreen or Category component?
# Actually, the button is in the TeamsScreen or DrawScreen?
# No, `handleReload` was in the App body or component body.
# Let's just write the modified content back.
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched frontend")
