import sys

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the start of App()
app_idx = text.find('export default function App')

# We only need the code BEFORE app_idx!
clean_top = text[:app_idx]

# I will write the App() function myself.
app_code = """export default function App() {
  const [categories, setCategories] = useState<Category[]>([])
  const [activeCatId, setActiveCatId] = useState<number | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('teams')
  const [loading, setLoading] = useState(true)
  const { toast, show } = useToast()
  
  const handleInitialReload = () => {
    setLoading(true)
    axios.post(`${API}/reload_teams`)
      .then(r => { show(r.data.message); fetchData() })
      .catch(e => show('Lỗi kết nối hoặc lỗi dữ liệu', 'error'))
      .finally(() => setLoading(false))
  }

  const fetchData = useCallback(() => {
    axios.get<Category[]>(`${API}/categories`)
      .then(r => {
        setCategories(r.data)
        setActiveCatId(prev => prev ?? (r.data[0]?.id ?? null))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const activeCategory = categories.find(c => c.id === activeCatId)
  const activeTeams = activeCategory?.teams ?? []

  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'teams',    label: 'Danh sách đội',  icon: '👥' },
    { id: 'draw',     label: 'Bốc thăm',      icon: '🎲' },
    { id: 'schedule', label: 'Lịch thi đấu',   icon: '📅' },
    { id: 'results',  label: 'Kết quả',       icon: '📊' },
    { id: 'search',   label: 'Tra cứu đa năng', icon: '🔍' }
  ]

  const catIcon = (c: Category) => c.sport === 'Bóng đá' ? '⚽' : '🏓'

  return (
    <div className="app-layout">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-logo-area">
          <img src="/logo_daihoi.png" alt="Logo Đại hội" style={{ height: 48, objectFit: 'contain' }} />
          <div className="header-title">
            <h1>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
            <small>Bóng đá Nam · Pickleball · Khu liên hợp thể thao Thanh Hà, Hà Nội</small>
          </div>
        </div>
        <div className="header-spacer" />
        <img src="/logo_mt_03.png" alt="Sponsor Logo" style={{ height: 48, objectFit: 'contain' }} />
      </header>

      {/* ── Nav Tabs ── */}
      <nav className="app-nav">
        {tabs.map(tab => (
          <button key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="nav-tab-icon">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      {/* ── Main Content ── */}
      <main className="main-content">
        {loading && categories.length === 0 ? (
          <div className="loading"><div className="spinner" /><span>Đang tải dữ liệu...</span></div>
          ) : categories.length === 0 ? (
            <div className="empty-state">
              {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
              <div className="empty-state-icon">📭</div>
              <h3>Chưa có dữ liệu</h3>
              <p>Danh sách giải đấu đang trống. Vui lòng kiểm tra lại file Excel và nhấn nút Cập nhật dưới đây.</p>
              <div style={{ marginTop: 20 }}>
                 <button className="btn btn-primary" onClick={handleInitialReload} disabled={loading}>
                   {loading ? "⏳ Đang xử lý..." : "🔄 Cập nhật dữ liệu từ Excel"}
                 </button>
              </div>
            </div>
        ) : (
          <>
            {/* Category pill selector */}
            {activeTab !== 'search' && (
            <div className="category-selector" style={{ marginBottom: 24 }}>
              {categories.map(cat => (
                <button key={cat.id}
                  className={`cat-btn ${cat.sport === 'Pickleball' ? 'sport-pick' : ''} ${activeCatId === cat.id ? 'active' : ''}`}
                  onClick={() => setActiveCatId(cat.id)}
                >
                  {catIcon(cat)} {cat.name}
                  <span className="cat-count">{cat.teams.length}</span>
                </button>
              ))}
            </div>
            )}
            
            {/* Active panel */}
            {activeCategory && activeTab !== 'search' && (
              <>
                {activeTab === 'draw' && (
                  <DrawScreen category={activeCategory} teams={activeTeams} onRefresh={fetchData} />
                )}
                {activeTab === 'teams' && (
                  <TeamsScreen category={activeCategory} teams={activeTeams} onRefresh={fetchData} />
                )}
                {activeTab === 'schedule' && (
                  <ScheduleScreen category={activeCategory} onRefresh={fetchData} />
                )}
                {activeTab === 'results' && (
                  <ResultsScreen category={activeCategory} onRefresh={fetchData} />
                )}
              </>
            )}
            {activeTab === 'search' && <GlobalSearchScreen categories={categories} />}
          </>
        )}
      </main>
    </div>
  )
}
"""

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(clean_top + app_code)
