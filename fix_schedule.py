import re

path = r"d:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Restore the top of ScheduleScreen
bad_start = content.find("// ─── SCHEDULE SCREEN")
bad_end = content.find("export function ScheduleScreen", bad_start)

if bad_start != -1 and bad_end != -1:
    content = content[:bad_start] + content[bad_end:]

# Now replace the variables
schedule_start = content.find("export function ScheduleScreen")
if schedule_start != -1:
    old_vars = "  const { isAdmin } = useAuth();\n\n\n  useEffect(() => { fetchMatches() }, [fetchMatches])"
    
    new_vars = """  const { isAdmin } = useAuth();
  const [matches, setMatches] = useState<Match[]>([])
  const [editId, setEditId] = useState<number | null>(null)
  const [editTime, setEditTime] = useState('')
  const [editCourt, setEditCourt] = useState('')
  const [genLoading, setGenLoading] = useState(false)
  const { toast, show } = useToast()

  const [filterCourt, setFilterCourt] = useState('')
  const [filterTime, setFilterTime] = useState('')
  const [sortBy, setSortBy] = useState('default')

  const fetchMatches = useCallback(() => {
    axios.get<Match[]>(`${API}/categories/${category.id}/matches`)
      .then(r => setMatches(r.data))
  }, [category.id])

  useEffect(() => { fetchMatches() }, [fetchMatches])"""
    
    content = content.replace(old_vars, new_vars)
    
# Now add the filtering logic
pending_logic = """  const pending = matches.filter(m => m.status !== 'completed')

  const completed = matches.filter(m => m.status === 'completed')"""

new_pending_logic = """  let filteredMatches = matches;
  if (filterCourt) {
    filteredMatches = filteredMatches.filter(m => (m.court || '').includes(filterCourt));
  }
  if (filterTime) {
    filteredMatches = filteredMatches.filter(m => (m.scheduled_time || '').includes(filterTime));
  }
  
  filteredMatches = [...filteredMatches].sort((a, b) => {
    if (sortBy === 'time_asc') return (a.scheduled_time || '').localeCompare(b.scheduled_time || '');
    if (sortBy === 'time_desc') return (b.scheduled_time || '').localeCompare(a.scheduled_time || '');
    if (sortBy === 'court_asc') return (a.court || '').localeCompare(b.court || '');
    if (sortBy === 'court_desc') return (b.court || '').localeCompare(a.court || '');
    return 0;
  });

  const pending = filteredMatches.filter(m => m.status !== 'completed')
  const completed = filteredMatches.filter(m => m.status === 'completed')

  const uniqueCourts = Array.from(new Set(matches.map(m => m.court).filter(Boolean))).sort();
  const uniqueTimes = Array.from(new Set(matches.map(m => m.scheduled_time).filter(Boolean))).sort();"""

content = content.replace(pending_logic, new_pending_logic)

# Now add the UI Header before pending list
header_injection = """      {pending.length > 0 && (

        <div className="schedule-day">"""

new_header = """      {matches.length > 0 && (
        <div style={{ background: 'white', borderRadius: 10, padding: '16px', marginTop: 16, marginBottom: 16, display: 'flex', gap: 16, flexWrap: 'wrap', boxShadow: 'var(--shadow)', alignItems: 'center' }}>
          <div style={{ fontWeight: 'bold' }}>Bộ lọc:</div>
          <select value={filterCourt} onChange={e => setFilterCourt(e.target.value)} className="input" style={{ width: 'auto', padding: '6px 12px' }}>
            <option value="">Tất cả địa điểm</option>
            {uniqueCourts.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={filterTime} onChange={e => setFilterTime(e.target.value)} className="input" style={{ width: 'auto', padding: '6px 12px' }}>
            <option value="">Tất cả khung giờ</option>
            {uniqueTimes.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <div style={{ fontWeight: 'bold', marginLeft: 16 }}>Sắp xếp:</div>
          <select value={sortBy} onChange={e => setSortBy(e.target.value)} className="input" style={{ width: 'auto', padding: '6px 12px' }}>
            <option value="default">Mặc định</option>
            <option value="time_asc">Khung giờ (Tăng dần)</option>
            <option value="time_desc">Khung giờ (Giảm dần)</option>
            <option value="court_asc">Sân (Tăng dần)</option>
            <option value="court_desc">Sân (Giảm dần)</option>
          </select>
        </div>
      )}

      {matches.length > 0 && (
        <div className="schedule-header-row" style={{ display: 'flex', padding: '12px 18px', background: 'var(--blue)', color: 'white', borderRadius: '8px', marginBottom: '8px', fontWeight: 'bold', gap: 14 }}>
           <div style={{ minWidth: '52px' }}>Giờ</div>
           <div style={{ minWidth: '65px' }}>Địa điểm</div>
           <div style={{ flex: 1, textAlign: 'center' }}>Đội thi đấu</div>
           <div style={{ minWidth: '80px', textAlign: 'center' }}>Tỷ số</div>
        </div>
      )}

      {pending.length > 0 && (

        <div className="schedule-day">"""

content = content.replace(header_injection, new_header)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done!")
