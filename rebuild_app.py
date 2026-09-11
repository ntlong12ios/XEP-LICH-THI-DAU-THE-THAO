import re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract everything up to GlobalSearchScreen (or App)
search_idx = text.find('function GlobalSearchScreen')
if search_idx == -1:
    print("Cannot find GlobalSearchScreen")

app_idx = text.find('export default function App')

# Part 1: imports and other components
header_text = text[:min(search_idx, app_idx)]

# 2. Extract GlobalSearchScreen
# It starts at search_idx and ends before APP ROOT
app_root_idx = text.find('// ─── APP ROOT', search_idx)
search_text = text[search_idx:app_root_idx]

# 3. Extract App
app_text = text[app_root_idx:]

# But wait, app_text might contain duplicates!
# We know the first App ends with } followed by EOF or another // ─── APP ROOT
next_root = app_text.find('// ─── APP ROOT', 100)
if next_root != -1:
    app_text = app_text[:next_root]
    
# Now we have header_text, search_text, app_text.
# Let's fix app_text to include the correct tabs array and activeTab === search logic.

# Fix tabs
tabs_regex = r"const tabs: \{ id: TabType; label: string; icon: string \}\[\] = \[.*?\]"
app_text = re.sub(tabs_regex, """const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'teams',    label: 'Danh sách đội',  icon: '👥' },
    { id: 'draw',     label: 'Bốc thăm',      icon: '🎲' },
    { id: 'schedule', label: 'Lịch thi đấu',   icon: '📅' },
    { id: 'results',  label: 'Kết quả',       icon: '📊' },
    { id: 'search',   label: 'Tra cứu đa năng', icon: '🔍' }
  ]""", app_text, flags=re.DOTALL)

# Fix catIcon
app_text = re.sub(r"const catIcon = \(c: Category\) => c\.sport === 'Bóng đá' \? '⚽' : '.*?'", 
                  "const catIcon = (c: Category) => c.sport === 'Bóng đá' ? '⚽' : '🏓'", app_text)

# Fix rendering
# First, remove any existing GlobalSearchScreen render to avoid duplicates
app_text = re.sub(r"\{activeTab === 'search' && <GlobalSearchScreen categories=\{categories\} />\}", "", app_text)

# Now inject it at the correct place
# The correct place is right before </main>
app_text = app_text.replace("</main>", "{activeTab === 'search' && <GlobalSearchScreen categories={categories} />}\n      </main>")

# Reassemble
final_text = header_text + "// ─── SEARCH SCREEN ────────────────────────────────────────────────────────\n" + search_text + "\n" + app_text

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Rebuild success!")
