import re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. TeamsScreen
text = text.replace('function TeamsScreen({ category, teams, onRefresh }: { category: Category; teams: Team[]; onRefresh: () => void }) {', 'function TeamsScreen({ category, teams, onRefresh }: { category: Category; teams: Team[]; onRefresh: () => void }) {\\n  const { isAdmin } = useAuth();')
text = text.replace('<button className="btn btn-secondary" onClick={handleReload} disabled={loading}>', '{isAdmin && <button className="btn btn-secondary" onClick={handleReload} disabled={loading}>')
text = text.replace('Cập nhật thông tin đội\\n\\n        </button>', 'Cập nhật thông tin đội\\n\\n        </button>)}')
text = text.replace('<button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>', '{isAdmin && <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>}')
text = text.replace('<button className="btn btn-secondary" onClick={() => {', '{isAdmin && <button className="btn btn-secondary" onClick={() => {')
text = text.replace('}}>📊 Xuất Excel</button>', '}}>📊 Xuất Excel</button>}')
# Hide athletes for football if not admin
text = text.replace('{team.athletes.map(a => (', '{(!isFootball || isAdmin) && team.athletes.map(a => (')

# 2. DrawScreen
text = text.replace('function DrawScreen({ category, teams, onRefresh }: {\\n\\n  category: Category; teams: Team[]; onRefresh: () => void\\n\\n}) {', 'function DrawScreen({ category, teams, onRefresh }: {\\n  category: Category; teams: Team[]; onRefresh: () => void\\n}) {\\n  const { isAdmin } = useAuth();')

# 3. ScheduleScreen
text = text.replace('function ScheduleScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {', 'function ScheduleScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {\\n  const { isAdmin } = useAuth();')

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Screens patched!")
