import re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

search_component = '''
// ─── SEARCH SCREEN ────────────────────────────────────────────────────────
function GlobalSearchScreen({ categories }: { categories: Category[] }) {
  const [matches, setMatches] = useState<Match[]>([])
  const [search, setSearch] = useState('')
  const [filterTime, setFilterTime] = useState('')
  const [filterCourt, setFilterCourt] = useState('')
  const [filterCat, setFilterCat] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    axios.get<Match[]>(`${API}/matches`)
      .then(r => setMatches(r.data))
      .catch(e => console.error(e))
      .finally(() => setLoading(false))
  }, [])

  const buildTooltip = (t: Team | null) => {
    if (!t) return ""
    let res = `Đội: ${t.name}`
    if (t.athletes && t.athletes.length > 0) {
      res += `\\nVĐV: ${t.athletes.map(a => a.name).join(' & ')}`
    }
    return res
  }

  const filteredMatches = matches.filter(m => {
    const q = search.toLowerCase()
    const matchCat = categories.find(c => c.id === m.category_id)
    
    // Search by athlete name, team name, match code
    let textMatch = false
    if (!q) textMatch = true
    else {
      textMatch = m.match_code.toLowerCase().includes(q) ||
                  (m.team1?.name?.toLowerCase().includes(q) ?? false) ||
                  (m.team2?.name?.toLowerCase().includes(q) ?? false) ||
                  (m.team1?.athletes?.some(a => a.name.toLowerCase().includes(q)) ?? false) ||
                  (m.team2?.athletes?.some(a => a.name.toLowerCase().includes(q)) ?? false) ||
                  (matchCat?.name?.toLowerCase().includes(q) ?? false)
    }

    const timeMatch = filterTime ? (m.scheduled_time === filterTime) : true
    const courtMatch = filterCourt ? (m.court?.toLowerCase().includes(filterCourt.toLowerCase())) : true
    const catMatch = filterCat ? (m.category_id.toString() === filterCat) : true

    return textMatch && timeMatch && courtMatch && catMatch
  })

  // Unique times and courts for filters
  const uniqueTimes = Array.from(new Set(matches.map(m => m.scheduled_time).filter(Boolean))).sort() as string[]
  const uniqueCourts = Array.from(new Set(matches.map(m => m.court).filter(Boolean))).sort() as string[]

  return (
    <div>
      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap', alignItems: 'center' }}>
        <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>
        <button className="btn btn-secondary" onClick={() => {
            const data = filteredMatches.map((m, i) => {
                const cat = categories.find(c => c.id === m.category_id)
                return {
                    'STT': i + 1,
                    'Nội dung': cat ? cat.name : '',
                    'Giờ': m.scheduled_time || '',
                    'Sân': m.court || '',
                    'Trận': m.match_code,
                    'Đội 1': m.team1 ? m.team1.name : '?',
                    'Đội 2': m.team2 ? m.team2.name : '?'
                }
            });
            exportToExcel(data, `TraCuu_${new Date().getTime()}`);
        }}>📊 Xuất Excel</button>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
        <div className="search-box" style={{ minWidth: 250 }}>
          <span>🔍</span>
          <input className="search-input" placeholder="Tìm VĐV, tên đội, trận..."
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        
        <select className="search-input" value={filterCat} onChange={e => setFilterCat(e.target.value)}>
          <option value="">-- Tất cả nội dung --</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>

        <select className="search-input" value={filterTime} onChange={e => setFilterTime(e.target.value)}>
          <option value="">-- Tất cả khung giờ --</option>
          {uniqueTimes.map(t => <option key={t} value={t}>{t}</option>)}
        </select>

        <select className="search-input" value={filterCourt} onChange={e => setFilterCourt(e.target.value)}>
          <option value="">-- Tất cả sân/địa điểm --</option>
          {uniqueCourts.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        
        <div className="section-badge" style={{marginLeft: 'auto'}}>
          ✅ Tìm thấy {filteredMatches.length} trận
        </div>
      </div>

      <div className="schedule-timeline">
        {loading ? <div className="loading"><div className="spinner" /><span>Đang tải...</span></div> : (
          filteredMatches.length === 0 ? <div className="empty-state" style={{padding:40}}>Không tìm thấy kết quả phù hợp</div> :
          filteredMatches.map(match => {
            const cat = categories.find(c => c.id === match.category_id)
            return (
              <div key={match.id} className="schedule-match-row" style={{ marginBottom: 12, padding: 16 }}>
                <div className="schedule-time">
                  {match.scheduled_time || <span style={{ color: '#ccc' }}>—:—</span>}
                </div>
                <div className="schedule-court" style={{ minWidth: 100 }}>
                  {match.court || <span style={{ opacity: 0.5 }}>—</span>}
                </div>
                
                <div className="schedule-match-info" style={{ display: 'flex', alignItems: 'center', flex: 1, gap: 16 }}>
                  <div style={{ minWidth: 160 }}>
                    <div style={{ fontSize: 11, color: '#888', marginBottom: 4, textTransform: 'uppercase', fontWeight: 600 }}>{cat?.name}</div>
                    <div className="schedule-match-teams">
                      <span className="team-name-sched" title={buildTooltip(match.team1)}>
                        {match.team1?.draw_code || match.team1?.name || '?'}
                      </span>
                      <strong style={{ color: 'var(--red)', margin: '0 6px' }}>vs</strong>
                      <span className="team-name-sched" title={buildTooltip(match.team2)}>
                        {match.team2?.draw_code || match.team2?.name || '?'}
                      </span>
                    </div>
                    <div className="schedule-match-code">{match.match_code}</div>
                  </div>
                  
                  <div className="schedule-match-athletes" style={{ flex: 1, borderLeft: '1px solid #eee', paddingLeft: 16 }}>
                    <div style={{ fontSize: 12, color: '#555', marginBottom: 2 }}>
                       <span style={{fontWeight: 600, color: 'var(--blue)'}}>{match.team1?.draw_code || 'Đội 1'}:</span> {match.team1?.athletes.map(a => a.name).join(' & ') || match.team1?.name || '—'}
                    </div>
                    <div style={{ fontSize: 12, color: '#555' }}>
                       <span style={{fontWeight: 600, color: 'var(--blue)'}}>{match.team2?.draw_code || 'Đội 2'}:</span> {match.team2?.athletes.map(a => a.name).join(' & ') || match.team2?.name || '—'}
                    </div>
                  </div>
                </div>
                
                {/* Result */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0, minWidth: 80, justifyContent: 'flex-end' }}>
                  {match.status === 'completed' && (
                    <span style={{ fontWeight: 700, fontSize: 15, color: 'var(--teal)' }}>{match.score1}–{match.score2}</span>
                  )}
                  <span className={`status-badge ${match.status}`}>
                    {match.status === 'completed' ? '✓' : match.status === 'playing' ? '▶' : '⏳'}
                  </span>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
'''

content = content.replace('// ─── APP ROOT ────────────────────────────────────────────────────────────', search_component + '\n// ─── APP ROOT ────────────────────────────────────────────────────────────')

# Update TabType
content = content.replace("type TabType = 'draw' | 'teams' | 'results' | 'schedule'", "type TabType = 'draw' | 'teams' | 'results' | 'schedule' | 'search'")

# Update tabs array
tabs_orig = '''  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'teams',    label: 'Danh sách đội',  icon: '👥' },
    { id: 'draw',     label: 'Bốc thăm',      icon: '🎲' },
    { id: 'schedule', label: 'Lịch thi đấu',   icon: '📅' },
    { id: 'results',  label: 'Kết quả',       icon: '📊' }
  ]'''
tabs_new = '''  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'search',   label: 'Tra cứu đa năng',icon: '🔍' },
    { id: 'teams',    label: 'Danh sách đội',  icon: '👥' },
    { id: 'draw',     label: 'Bốc thăm',      icon: '🎲' },
    { id: 'schedule', label: 'Lịch thi đấu',   icon: '📅' },
    { id: 'results',  label: 'Kết quả',       icon: '📊' }
  ]'''
if tabs_orig in content:
    content = content.replace(tabs_orig, tabs_new)
else:
    print("Tabs orig not found")

# Mount active component
active_comp_orig = '''{activeTab === 'results' && <ResultsScreen category={activeCategory} onRefresh={fetchData} />}'''
active_comp_new = '''{activeTab === 'search' && <GlobalSearchScreen categories={categories} />}
                {activeTab === 'results' && <ResultsScreen category={activeCategory} onRefresh={fetchData} />}'''
content = content.replace(active_comp_orig, active_comp_new)

# When rendering tabs, if search is active, do not render category pill selector
content = content.replace('{/* Category pill selector */}', '{/* Category pill selector */}\n            {activeTab !== \'search\' && (')
content = content.replace('{/* Active panel */}', ')}\n            {/* Active panel */}')

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Script finished')
