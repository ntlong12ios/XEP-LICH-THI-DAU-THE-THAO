import { useEffect, useState, useCallback, useRef } from 'react'


import { createContext, useContext } from 'react';

export const AuthContext = createContext({ isAdmin: false });
export const useAuth = () => useContext(AuthContext);

const projectToLed = (type: string, data: any) => {
    axios.post('http://' + window.location.hostname + ':8000/led_state', { type, data })
         .then(() => alert("Đã chuyển tín hiệu lên màn LED"))
         .catch(() => alert("Lỗi kết nối màn LED"))
};

import axios from 'axios'

import { exportToExcel, printToPDF } from './utils/exportUtils'

import './App.css'



const API = import.meta.env.PROD ? '/api' : `http://${window.location.hostname}:8000`



// ─── Types ─────────────────────────────────────────────────────────────

interface Athlete { id: number; name: string; team_id: number }



interface Team {

  id: number; name: string

  contact_name: string | null; contact_phone: string | null

  draw_code: string | null; category_id: number

  athletes: Athlete[]

}



interface Category { id: number; name: string; sport: string; teams: Team[] }



interface BracketSlot {

  id: number; category_id: number; slot_code: string

  round_number: number; match_number: number

  slot_index: number; position_in_match: number

  label: string | null; team_id: number | null; team: Team | null

}



interface Match {

  id: number; match_code: string; category_id: number

  team1_id: number | null; team2_id: number | null

  score1: number | null; score2: number | null

  status: string; next_match_id: number | null

  scheduled_time: string | null; court: string | null

  team1: Team | null; team2: Team | null

}



type TabType = 'draw' | 'teams' | 'results' | 'schedule' | 'search'



// ─── Toast hook ─────────────────────────────────────────────────────────

function useToast() {

  const [toast, setToast] = useState<{ msg: string; type: string } | null>(null)

  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const show = useCallback((msg: string, type = 'success') => {

    if (timerRef.current) clearTimeout(timerRef.current)

    setToast({ msg, type })

    timerRef.current = setTimeout(() => setToast(null), 3000)

  }, [])

  return { toast, show }

}



// ─── DRAW SCREEN ────────────────────────────────────────────────────────

export function DrawScreen({ category, teams, onRefresh }: {

  category: Category; teams: Team[]; onRefresh: () => void

}) {
  const { isAdmin } = useAuth();

  const [slots, setSlots] = useState<BracketSlot[]>([])

  const [loading, setLoading] = useState(false)

  const [search, setSearch] = useState('')

  const { toast, show } = useToast()

  const isFootball = category.sport === 'Bóng đá'



  const fetchSlots = useCallback(() => {

    axios.get<BracketSlot[]>(`${API}/categories/${category.id}/bracket_slots`)

      .then(r => setSlots(r.data))

      .catch(() => setSlots([]))

  }, [category.id])



  useEffect(() => { fetchSlots() }, [fetchSlots])



  const [drawFormat, setDrawFormat] = useState('knockout')

  const [numGroups, setNumGroups] = useState(8)



  const generateBracket = () => {

    setLoading(true)

    axios.post(`${API}/categories/${category.id}/generate_bracket`, {

      format: drawFormat,

      num_groups: numGroups

    })

      .then(() => { fetchSlots(); show('Đã tạo sơ đồ bốc thăm!') })

      .catch(() => show('Lỗi tạo sơ đồ!', 'error'))

      .finally(() => setLoading(false))

  }



  const assignTeam = (slotId: number, teamId: number | null) => {

    const req = teamId === null

      ? axios.delete(`${API}/bracket_slots/${slotId}/assign`)

      : axios.put(`${API}/bracket_slots/${slotId}/assign`, { team_id: teamId })

    req.then(() => { fetchSlots(); onRefresh() })

       .catch(() => show('Lỗi cập nhật!', 'error'))

  }



  // Group slots by match_number

  const matchGroups: Record<number, BracketSlot[]> = {}

  for (const s of slots) {

    if (!matchGroups[s.match_number]) matchGroups[s.match_number] = []

    matchGroups[s.match_number].push(s)

  }



  const assignedIds = new Set(slots.filter(s => s.team_id).map(s => s.team_id!))

  const unassigned = teams.filter(t => !assignedIds.has(t.id))

  const assignedCount = assignedIds.size

  const orderedSlots = slots.slice().sort((a, b) => {
    if (a.match_number !== b.match_number) return a.match_number - b.match_number;
    return a.position_in_match - b.position_in_match;
  });
  const getGlobalSlotNum = (slotId: number) => {
    const idx = orderedSlots.findIndex(s => s.id === slotId);
    return idx >= 0 ? idx + 1 : 0;
  };



  const filteredEntries = Object.entries(matchGroups).filter(([, slist]) => {

    if (!search) return true

    const q = search.toLowerCase()

    return slist.some(s =>

      s.slot_code?.toLowerCase().includes(q) ||

      s.team?.name?.toLowerCase().includes(q) ||

      s.team?.draw_code?.toLowerCase().includes(q)

    )

  })



  return (

    <div className="draw-container">

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}



      {/* Stats row */}

      <div className="draw-stats">

        <div className="stat-card red">

          <div className="stat-value">{teams.length}</div>

          <div className="stat-label">Tổng số đội</div>

        </div>

        <div className="stat-card teal">

          <div className="stat-value">{assignedCount}</div>

          <div className="stat-label">Đã bốc thăm</div>

        </div>

        <div className="stat-card orange">

          <div className="stat-value">{unassigned.length}</div>

          <div className="stat-label">Chưa bốc thăm</div>

        </div>

        <div className="stat-card blue">

          <div className="stat-value">{Object.keys(matchGroups).length}</div>

          <div className="stat-label">Số trận Vòng 1</div>

        </div>

      </div>



      {/* Info banner */}

      {unassigned.length > 0 && slots.length > 0 && (

        <div className="draw-info-bar">

          <span>⚡</span>

          <div>

            Còn <strong>{unassigned.length}</strong> đội chưa bốc thăm.

            {' '}Chọn từ dropdown trong từng ô để gán vào sơ đồ. Đổi chỗ 2 đội: chọn đội sang ô khác → hệ thống tự hoán vị.

          </div>

        </div>

      )}



      {/* Controls */}

      <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap', marginBottom: 12 }}>

        {isAdmin && <select className="search-input" style={{ width: 220 }} value={drawFormat} onChange={e => setDrawFormat(e.target.value)}>

          <option value="knockout">Đấu loại trực tiếp (Bắt cặp)</option>

          <option value="round_robin">Chia bảng (Đấu vòng tròn)</option>
        </select>}

        {isAdmin && drawFormat === 'round_robin' && (

          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>

            <span style={{ fontWeight: 600, fontSize: 14 }}>Số bảng:</span>

            <input type="number" className="search-input" style={{ width: 70, textAlign: 'center' }} 

              value={numGroups} onChange={e => setNumGroups(parseInt(e.target.value) || 8)} min={1} max={32} />

          </div>

        )}

        {isAdmin && <button className="btn btn-primary" onClick={generateBracket} disabled={loading}>

          {loading ? '⏳' : '🎲'} {slots.length > 0 ? 'Tạo lại sơ đồ' : 'Tạo sơ đồ bốc thăm'}

        </button>}

        {isAdmin && <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>}
        {isAdmin && <button className="btn btn-secondary" style={{backgroundColor: '#1565C0', color: 'white', borderColor: '#1565C0'}} onClick={() => projectToLed('all_brackets', { categoryId: category.id, drawFormat, isFootball: category.name.toLowerCase().includes('bóng đá') })}>📺 Chiếu toàn bộ LED</button>}

        {isAdmin && <button className="btn btn-secondary" onClick={() => {

            const data = filteredEntries.map(([matchNum, slots]) => {

                const groupName = `Bảng ${matchNum}`;

                return slots.map(s => ({

                    'Bảng/Cặp': groupName,

                    'Vị trí': s.position_in_match,

                    'Mã bốc thăm': s.slot_code,

                    'Tên đội': s.team ? s.team.name : '---'

                }));

            }).flat();

            exportToExcel(data, `BocTham_${category.name}`);

        }}>📊 Xuất Excel</button>}

        {slots.length > 0 && (

          <>

            <div className="search-box">

              <span>🔍</span>

              <input className="search-input"

                placeholder="Tìm trận hoặc mã đội..."

                value={search}

                onChange={e => setSearch(e.target.value)}

              />

              {search && (

                <button style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#999' }}

                  onClick={() => setSearch('')}>✕</button>

              )}

            </div>

            <span className="section-badge">

              {Object.keys(matchGroups).length} trận · {assignedCount}/{teams.length * 2} slot đã gán

            </span>

          </>

        )}

      </div>



      {slots.length === 0 ? (

        <div className="empty-state card">

          <div className="empty-state-icon">🎯</div>

          <h3>Chưa có sơ đồ bốc thăm</h3>

          <p>Nhấn <strong>"Tạo sơ đồ bốc thăm"</strong> để khởi tạo các ô trận dựa trên {teams.length} đội.</p>

        </div>

      ) : (

        <div className="bracket-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))' }}>

          {filteredEntries.map(([matchNum, slotList]) => {

            const sorted = [...slotList].sort((a, b) => a.position_in_match - b.position_in_match)

            const code = sorted[0]?.label || sorted[0]?.slot_code || `Trận ${matchNum}`

            const bothAssigned = sorted.every(s => s.team_id)

            return (

              <div key={matchNum} className={`match-card ${bothAssigned ? 'match-card-complete' : ''}`}>

                <div className={`match-header ${isFootball ? 'football' : 'pickleball'}`}>

                  <span>{isFootball ? '⚽' : '🏓'} {code}</span>
                  {isAdmin && <button className='btn-sm btn-ghost' style={{color:'white', borderColor:'white', marginLeft: 10}} onClick={(e)=>{e.stopPropagation(); projectToLed('bracket', {matchNum, slotList, category, isFootball})}}>📺 Chiếu LED</button>}

                  <span style={{ fontSize: 11, opacity: 0.85 }}>

                    {bothAssigned ? '✅ Đủ đội' : `${sorted.filter(s => s.team_id).length}/${sorted.length} đội`}

                  </span>

                </div>

                {sorted.map((slot, pos) => {

                  const isAssigned = !!slot.team_id

                  // Build option list: unassigned teams + current team in this slot

                  const opts = [

                    ...unassigned,

                    ...(slot.team ? [slot.team] : [])

                  ].filter((t, i, arr) => arr.findIndex(x => x.id === t.id) === i)



                  return (

                    <div key={slot.id} className={`match-slot ${isAssigned ? 'slot-assigned' : ''}`}>

                      {/* Position label */}

                      <div className="slot-position" style={{display: 'flex', flexDirection: 'column'}}>
                        <span>Đội {pos + 1}</span>
                        <span style={{color: '#d32f2f', fontWeight: 'bold', fontSize: '1.1rem', marginTop: 12, marginBottom: 12}}>
                          Số {getGlobalSlotNum(slot.id).toString().padStart(2, '0')}
                        </span>
                      </div>



                      {/* Draw code badge */}

                      <span className={`slot-code-badge ${isAssigned ? 'badge-assigned' : 'badge-empty'}`}>

                        {slot.team?.draw_code || (isAssigned ? '✓' : '—')}

                      </span>



                      {/* Team selector */}

                      <select

                        className="slot-select"

                        value={slot.team_id ?? ''}

                        onChange={e => assignTeam(slot.id, e.target.value ? parseInt(e.target.value) : null)}

                        title={slot.team?.name || ''}

                      >

                        <option value="">-- Chưa bốc thăm --</option>

                        {opts.map(t => (

                          <option key={t.id} value={t.id}>

                            {t.draw_code && t.draw_code !== t.name ? `[${t.draw_code}] ` : ''}

                            {t.name}

                          </option>

                        ))}

                      </select>



                      {/* Unassign button */}

                      {isAssigned && isAdmin && (<button className="btn-unassign" title="Xóa gán"

                          onClick={() => assignTeam(slot.id, null)}>✕</button>

                      )}

                      

                      {/* Athletes preview */}

                      {isAssigned && slot.team && slot.team.athletes.length > 0 && (

                        <div className="slot-athletes">

                          VĐV: {slot.team.athletes.map(a => a.name).join(' & ')}

                        </div>

                      )}

                    </div>

                  )

                })}

              </div>

            )

          })}

        </div>

      )}

    </div>

  )

}



// ─── TEAMS SCREEN ────────────────────────────────────────────────────────

function TeamsScreen({ category, teams, onRefresh }: { category: Category; teams: Team[]; onRefresh: () => void }) {
  const { isAdmin } = useAuth();
  const [search, setSearch] = useState('')

  const [loading, setLoading] = useState(false)

  const { toast, show } = useToast()

  const isFootball = category.sport === 'Bóng đá'



  const handleReload = () => {

    if (!window.confirm('Cập nhật lại từ file Excel sẽ ghi đè toàn bộ danh sách đội và bốc thăm hiện tại. Bạn có chắc chắn không?')) return

    

    setLoading(true)

    axios.post(`${API}/reload_teams`)

      .then(r => {

        show(r.data.message)

        onRefresh()

      })

      .catch(e => {

        const detail = e.response?.data?.detail || 'Lỗi cập nhật dữ liệu!'

        show(detail, 'error')

      })

      .finally(() => setLoading(false))

  }



  const filtered = teams.filter(t => {

    if (!search) return true

    const q = search.toLowerCase()

    return t.name.toLowerCase().includes(q)

      || t.draw_code?.toLowerCase().includes(q)

      || t.athletes.some(a => a.name.toLowerCase().includes(q))

      || t.contact_name?.toLowerCase().includes(q)

  })



  const assigned = filtered.filter(t => t.draw_code && t.draw_code !== 'nan')

  const unassigned = filtered.filter(t => !t.draw_code || t.draw_code === 'nan')



  return (

    <div>

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}

      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap', alignItems: 'center' }}>

        {isAdmin && <button className="btn btn-secondary" onClick={handleReload} disabled={loading}>

          {loading ? '⏳' : '🔄'} Cập nhật thông tin đội
        </button>}

        {isAdmin && <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>}

        {isAdmin && <button className="btn btn-secondary" onClick={() => {

            const data = filtered.map((t, i) => ({

              'STT': i + 1,

              'Mã bốc thăm': t.draw_code || '',

              'Tên đội': t.name,

              'Vận động viên': t.athletes?.map(a => a.name).join(', ') || '',

              'Liên hệ': t.contact_name || '',

              'SĐT': t.contact_phone || ''

            }));

            exportToExcel(data, `DanhSachDoi_${category.name}`);

        }}>📊 Xuất Excel</button>}

        <div className="search-box">

          <span>🔍</span>

          <input className="search-input"

            placeholder="Tìm theo tên đội, VĐV, mã bốc thăm..."

            value={search}

            onChange={e => setSearch(e.target.value)}

          />

          {search && (

            <button style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#999' }}

              onClick={() => setSearch('')}>✕</button>

          )}

        </div>

        <span className="section-badge">✅ {assigned.length} đã có mã · ⏳ {unassigned.length} chưa có</span>

      </div>



      <div className="card">

        <div className="teams-table-wrap">

          <table className={`teams-table ${isFootball ? '' : 'pick'}`}>

            <thead>

              <tr>

                <th style={{ width: 40 }}>#</th>

                <th style={{ width: 120 }}>Mã bốc thăm</th>

                <th>Tên đội / Đơn vị</th>

                <th>{isFootball ? 'Vận động viên' : 'Cặp đôi (VĐV)'}</th>

                <th style={{ width: 140 }}>Người liên hệ</th>

                <th style={{ width: 130 }}>Điện thoại</th>

              </tr>

            </thead>

            <tbody>

              {filtered.map((team, idx) => {

                const hasCode = team.draw_code && team.draw_code !== 'nan'

                return (

                  <tr key={team.id}>

                    <td style={{ color: 'var(--text-muted)', fontWeight: 600, textAlign: 'center' }}>{idx + 1}</td>

                    <td>

                      <span className={`draw-code-chip ${hasCode ? 'assigned' : 'unassigned'}`}>

                        {hasCode ? team.draw_code : 'Chưa có'}

                      </span>

                    </td>

                    <td style={{ fontWeight: 600 }}>{team.name}</td>

                    <td>

                      <div className="athlete-tags">

                        {(!isFootball || isAdmin) && team.athletes.map(a => (

                          <span key={a.id} className="athlete-tag">{a.name}</span>

                        ))}

                        {team.athletes.length === 0 && <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>—</span>}

                      </div>

                    </td>

                    <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>{team.contact_name || '—'}</td>

                    <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>{team.contact_phone || '—'}</td>

                  </tr>

                )

              })}

              {filtered.length === 0 && (

                <tr><td colSpan={6} style={{ textAlign: 'center', padding: 32, color: 'var(--text-muted)' }}>Không tìm thấy kết quả</td></tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  )

}



// ─── RESULTS SCREEN ──────────────────────────────────────────────────────

export function ResultsScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {
  const { isAdmin } = useAuth();
  console.log(isAdmin);
  const [matches, setMatches] = useState<Match[]>([])

  const [editScores, setEditScores] = useState<Record<number, { s1: string; s2: string }>>({})

  const [search, setSearch] = useState('')

  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')

  const { toast, show } = useToast()



  const fetchMatches = useCallback(() => {

    axios.get<Match[]>(`${API}/categories/${category.id}/matches`)

      .then(r => setMatches(r.data))

      .catch(() => setMatches([]))

  }, [category.id])



  useEffect(() => { fetchMatches() }, [fetchMatches])



  const saveScore = (match: Match) => {

    const ed = editScores[match.id]

    if (!ed) return

    const s1 = parseInt(ed.s1)

    const s2 = parseInt(ed.s2)

    if (isNaN(s1) || isNaN(s2) || s1 < 0 || s2 < 0) {

      show('Vui lòng nhập điểm số hợp lệ!', 'error')

      return

    }

    axios.put(`${API}/matches/${match.id}/score`, { score1: s1, score2: s2 })

      .then(() => {

        fetchMatches()

        setEditScores(prev => { const n = { ...prev }; delete n[match.id]; return n })

        show('Đã lưu kết quả! ✓')

        onRefresh()

      })

      .catch(() => show('Lỗi lưu kết quả!', 'error'))

  }



  const startEdit = (match: Match) => {

    setEditScores(prev => ({

      ...prev,

      [match.id]: {

        s1: match.score1 !== null ? String(match.score1) : '',

        s2: match.score2 !== null ? String(match.score2) : '',

      }

    }))

  }



  const cancelEdit = (matchId: number) => {

    setEditScores(prev => { const n = { ...prev }; delete n[matchId]; return n })

  }



  const filtered = matches.filter(m => {

    if (filter === 'pending' && m.status === 'completed') return false

    if (filter === 'completed' && m.status !== 'completed') return false

    if (!search) return true

    const q = search.toLowerCase()

    return m.match_code.toLowerCase().includes(q)

      || m.team1?.name?.toLowerCase().includes(q)

      || m.team2?.name?.toLowerCase().includes(q)

  })



  const completedCount = matches.filter(m => m.status === 'completed').length

  const statusLabel: Record<string, string> = { pending: 'Chưa đấu', playing: 'Đang đấu', completed: 'Hoàn thành' }



  return (

    <div>

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}



      {/* Controls */}

      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap', alignItems: 'center' }}>

        {matches.length > 0 && (

          <>

            <div style={{ display: 'flex', gap: 4 }}>

              {(['all', 'pending', 'completed'] as const).map(f => (

                <button key={f}

                  className={`btn btn-sm ${filter === f ? 'btn-secondary' : 'btn-ghost'}`}

                  onClick={() => setFilter(f)}

                >

                  {f === 'all' ? 'Tất cả' : f === 'pending' ? 'Chưa đấu' : 'Hoàn thành'}

                </button>

              ))}

            </div>

            <div className="search-box">

              <span>🔍</span>

              <input className="search-input" placeholder="Tìm trận, đội..."

                value={search} onChange={e => setSearch(e.target.value)} />

            </div>

            {isAdmin && <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>}

            {isAdmin && <button className="btn btn-secondary" onClick={() => {

                const data = matches.map((m, i) => ({

                    'STT': i + 1,

                    'Trận': m.match_code,

                    'Đội 1': m.team1 ? m.team1.name : '?',

                    'Điểm 1': m.score1 !== null ? m.score1 : '',
                    'Điểm 2': m.score2 !== null ? m.score2 : '',

                    'Đội 2': m.team2 ? m.team2.name : '?',

                    'Trạng thái': m.status === 'completed' ? 'Đã xong' : 'Chưa đấu'

                }));

                exportToExcel(data, `KetQua_${category.name}`);

            }}>📊 Xuất Excel</button>}

            <span className="section-badge">

              ✅ {completedCount}/{matches.length} trận xong

            </span>

          </>

        )}

      </div>



      {matches.length === 0 ? (

        <div className="empty-state card">

          <div className="empty-state-icon">📋</div>

          <h3>Chưa có trận đấu</h3>

          <p>Vào tab <strong>"Lịch thi đấu"</strong> để tạo lịch trước.</p>

        </div>

      ) : (

        <div className="matches-grid">

          {filtered.map(match => {

            const ed = editScores[match.id]

            const s1 = match.score1 ?? null

            const s2 = match.score2 ?? null

            const isCompleted = match.status === 'completed'

            const winner = isCompleted ? (s1! > s2! ? 'team1' : s2! > s1! ? 'team2' : 'draw') : null



            return (

              <div key={match.id} className={`result-card ${isCompleted ? 'result-card-done' : ''}`}>

                <div className={`result-card-header ${match.status}`}>

                  <span>{category.sport === 'Bóng đá' ? '⚽' : '🏓'} {match.match_code}</span>

                  <span className={`status-badge ${match.status}`}>{statusLabel[match.status]}</span>

                </div>

                <div className="result-card-body">

                  {/* Teams */}

                  <div className="match-teams">

                    <div className={`match-team ${winner === 'team1' ? 'team-winner' : winner ? 'team-loser' : ''}`}>

                      <div className="match-team-name">

                        {match.team1?.draw_code && match.team1.draw_code !== match.team1.name

                          ? <span className="draw-code-inline">{match.team1.draw_code}</span>

                          : null}

                        {match.team1?.name || (match.team1_id ? `Đội #${match.team1_id}` : '—')}

                      </div>

                      <div className="match-team-athletes">

                        {match.team1?.athletes.map(a => a.name).join(' & ') || ''}

                      </div>

                      {winner === 'team1' && <div className="winner-crown">🏆 Thắng</div>}

                    </div>

                    <div className="match-vs">VS</div>

                    <div className={`match-team ${winner === 'team2' ? 'team-winner' : winner ? 'team-loser' : ''}`}>

                      <div className="match-team-name">

                        {match.team2?.draw_code && match.team2.draw_code !== match.team2.name

                          ? <span className="draw-code-inline">{match.team2.draw_code}</span>

                          : null}

                        {match.team2?.name || (match.team2_id ? `Đội #${match.team2_id}` : '—')}

                      </div>

                      <div className="match-team-athletes">

                        {match.team2?.athletes.map(a => a.name).join(' & ') || ''}

                      </div>

                      {winner === 'team2' && <div className="winner-crown">🏆 Thắng</div>}

                    </div>

                  </div>



                  {/* Score input */}

                  {ed ? (

                    <div>

                      <div className="score-row">

                        <input type="number" min={0} className="score-input"

                          value={ed.s1}

                          onChange={e => setEditScores(prev => ({ ...prev, [match.id]: { ...prev[match.id], s1: e.target.value } }))}

                          placeholder="0" autoFocus />

                        <span className="score-dash">—</span>

                        <input type="number" min={0} className="score-input"

                          value={ed.s2}

                          onChange={e => setEditScores(prev => ({ ...prev, [match.id]: { ...prev[match.id], s2: e.target.value } }))}

                          placeholder="0" />

                      </div>

                      <div style={{ marginTop: 10, display: 'flex', gap: 8, justifyContent: 'flex-end' }}>

                        <button className="btn btn-ghost btn-sm" onClick={() => cancelEdit(match.id)}>Hủy</button>

                        <button className="btn btn-primary btn-sm" onClick={() => saveScore(match)}>💾 Lưu kết quả</button>

                      </div>

                    </div>

                  ) : (

                    <div>

                      {isCompleted && (

                        <div className="score-display">

                          <span className={winner === 'team1' ? 'score-win' : 'score-lose'}>{s1}</span>

                          <span className="score-sep">–</span>

                          <span className={winner === 'team2' ? 'score-win' : 'score-lose'}>{s2}</span>

                        </div>

                      )}

                      <div style={{ marginTop: isCompleted ? 8 : 12, display: 'flex', justifyContent: 'flex-end' }}>

                        {isAdmin && <button className="btn btn-outline btn-sm" onClick={() => startEdit(match)}>

                          {isCompleted ? '✏️ Sửa kết quả' : '📝 Nhập kết quả'}
                        </button>}

                      </div>

                    </div>

                  )}

                </div>

              </div>

            )

          })}



          {filtered.length === 0 && (

            <div style={{ gridColumn: '1/-1' }}>

              <div className="empty-state card">

                <div className="empty-state-icon">🔍</div>

                <h3>Không tìm thấy kết quả</h3>

              </div>

            </div>

          )}

        </div>

      )}

    </div>

  )

}



export function ScheduleScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {
  const { isAdmin } = useAuth();
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

  useEffect(() => { fetchMatches() }, [fetchMatches])



  const generateMatches = () => {

    setGenLoading(true)

    axios.post(`${API}/categories/${category.id}/generate_matches`)

      .then(r => {

        fetchMatches()

        show(`Đã tạo ${r.data.matches_created} trận đấu từ sơ đồ bốc thăm! 🎉`)

        onRefresh()

      })

      .catch(e => {

        const detail = e.response?.data?.detail || 'Lỗi tạo trận đấu!'

        show(detail, 'error')

      })

      .finally(() => setGenLoading(false))

  }



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



  const saveSchedule = (matchId: number) => {

    axios.put(`${API}/matches/${matchId}/schedule`, {

      scheduled_time: editTime || null,

      court: editCourt || null,

    }).then(() => { fetchMatches(); setEditId(null); show('Đã cập nhật lịch!') })

      .catch(() => show('Lỗi cập nhật!', 'error'))

  }



  const handlePrint = () => {

    window.print()

  }



  let filteredMatches = matches;
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
  const uniqueTimes = Array.from(new Set(matches.map(m => m.scheduled_time).filter(Boolean))).sort();

  const isFootball = category.sport === 'Bóng đá'



  const renderRow = (match: Match) => {

    const isEditing = editId === match.id

    const s1 = match.score1; const s2 = match.score2

    const winner = match.status === 'completed'

      ? (s1! > s2! ? match.team1?.name : s2! > s1! ? match.team2?.name : null)

      : null



    const buildTooltip = (t: Team | null) => {

      if (!t) return ""

      let res = `Đội: ${t.name}`

      if (t.athletes && t.athletes.length > 0) {

        res += `
VĐV: ${t.athletes.map(a => a.name).join(' & ')}`

      }

      return res

    }



    return (

      <div key={match.id} className="schedule-match-row">

        {/* Time */}

        {isEditing ? (

          <input type="time" className="schedule-time-input"

            value={editTime}

            onChange={e => setEditTime(e.target.value)} />

        ) : (

          <div className="schedule-time" onClick={() => { setEditId(match.id); setEditTime(match.scheduled_time || ''); setEditCourt(match.court || '') }}>

            {match.scheduled_time || <span style={{ color: '#ccc' }}>—:—</span>}

          </div>

        )}



        {/* Court */}

        {isEditing ? (

          <input className="schedule-court-input"

            placeholder="Sân..."

            value={editCourt}

            onChange={e => setEditCourt(e.target.value)} />

        ) : (

          <div className="schedule-court" onClick={() => { setEditId(match.id); setEditTime(match.scheduled_time || ''); setEditCourt(match.court || '') }}>

            {match.court || <span style={{ opacity: 0.5 }}>—</span>}

          </div>

        )}



        {/* Match info + Athletes details */}

        <div className="schedule-match-info" style={{ display: 'flex', alignItems: 'center', flex: 1, gap: 16 }}>

          <div style={{ minWidth: 160 }}>

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



        {/* Result / actions */}

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>

          {match.status === 'completed' && (

            <>

              <span style={{ fontWeight: 700, fontSize: 15, color: 'var(--teal)' }}>{s1}–{s2}</span>

              {winner && <span className="winner-label">🏆 {winner}</span>}

            </>

          )}

          {isEditing ? (

            <>

              <button className="btn btn-ghost btn-sm" onClick={() => setEditId(null)}>Hủy</button>

              <button className="btn btn-secondary btn-sm" onClick={() => saveSchedule(match.id)}>Lưu</button>

            </>

          ) : (

            <button className="btn btn-ghost btn-sm"

              onClick={() => { setEditId(match.id); setEditTime(match.scheduled_time || ''); setEditCourt(match.court || '') }}>

              ✏️

            </button>

          )}

          <span className={`status-badge ${match.status}`}>

            {match.status === 'completed' ? '✓' : match.status === 'playing' ? '▶' : '⏳'}

          </span>

        </div>

      </div>

    )

  }



  return (

    <div className="schedule-timeline">

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}



      <div style={{ display: 'flex', gap: 12, marginBottom: 4, alignItems: 'center', flexWrap: 'wrap' }}>

        

          <button className="btn" onClick={() => printToPDF()}><span className="btn-icon">📄</span> Xuất PDF</button>

          <button className="btn" onClick={() => {

              const data = matches.map((m, i) => ({

                  'STT': i + 1,

                  'Giờ': m.scheduled_time || '',

                  'Sân': m.court || '',

                  'Trận': m.match_code,

                  'Đội 1': m.team1 ? m.team1.name : '?',

                  'Đội 2': m.team2 ? m.team2.name : '?'

              }));

              exportToExcel(data, `LichThiDau_${category.name}`);

          }}><span className="btn-icon">📊</span> Xuất Excel</button>



          {isAdmin && <button className="btn btn-primary" onClick={generateMatches} disabled={genLoading}>
          {genLoading ? '⏳' : '⚡'} {matches.length > 0 ? 'Tạo lại lịch từ sơ đồ' : 'Tạo lịch từ sơ đồ bốc thăm'}
        </button>}

        {isAdmin && <label className="btn btn-secondary" style={{cursor: 'pointer', display: 'inline-flex', alignItems: 'center'}}>
          {genLoading ? '⏳' : '📥'} Tải Agenda từ Excel
          <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleAgendaUpload} disabled={genLoading} />
        </label>}

        <div style={{ flex: 1 }} />

        {isAdmin && <button className="btn btn-outline" onClick={handlePrint}>🖨️ In lịch thi đấu</button>}

      </div>



      {/* Legend */}

      {matches.length > 0 && (

        <div style={{ background: 'white', borderRadius: 10, padding: '10px 16px', fontSize: 12, color: 'var(--text-muted)', display: 'flex', gap: 16, flexWrap: 'wrap', boxShadow: 'var(--shadow)' }}>

          <span>💡 Nhấn vào giờ hoặc sân để chỉnh sửa trực tiếp</span>

          <span>· {isFootball ? '⚽ Bóng đá Nam' : '🏓 Pickleball'}</span>

          <span>· {matches.length} trận tổng</span>

        </div>

      )}



      {matches.length === 0 && (

        <div className="empty-state card">

          <div className="empty-state-icon">📅</div>

          <h3>Chưa có lịch thi đấu</h3>

          <p>Nhấn nút <strong>"Tạo lịch từ sơ đồ bốc thăm"</strong> ở trên để bắt đầu.</p>

        </div>

      )}



      {matches.length > 0 && (
        <div style={{ background: 'white', borderRadius: 10, padding: '16px', marginTop: 16, marginBottom: 16, display: 'flex', gap: 16, flexWrap: 'wrap', boxShadow: 'var(--shadow)', alignItems: 'center' }}>
          <div style={{ fontWeight: 'bold' }}>Bộ lọc:</div>
          <select value={filterCourt} onChange={e => setFilterCourt(e.target.value)} className="input" style={{ width: 'auto', padding: '6px 12px' }}>
            <option value="">Tất cả địa điểm</option>
            {uniqueCourts.map(c => <option key={c || ''} value={c || ''}>{c}</option>)}
          </select>
          <select value={filterTime} onChange={e => setFilterTime(e.target.value)} className="input" style={{ width: 'auto', padding: '6px 12px' }}>
            <option value="">Tất cả khung giờ</option>
            {uniqueTimes.map(t => <option key={t || ''} value={t || ''}>{t}</option>)}
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

        <div className="schedule-day">

          <div className="schedule-day-header">

            <span>⏳ Trận sắp đấu</span>

            <span style={{ fontSize: 13, opacity: 0.85 }}>{pending.length} trận</span>

          </div>

          {pending.map(renderRow)}

        </div>

      )}



      {completed.length > 0 && (

        <div className="schedule-day">

          <div className="schedule-day-header">

            <span>✅ Đã hoàn thành</span>

            <span style={{ fontSize: 13, opacity: 0.85 }}>{completed.length} trận</span>

          </div>

          {completed.map(renderRow)}

        </div>

      )}

    </div>

  )

}





// ─── SEARCH SCREEN ────────────────────────────────────────────────────────

// ─── SEARCH SCREEN ────────────────────────────────────────────────────────
function GlobalSearchScreen({ categories }: { categories: Category[] }) {
  const { isAdmin } = useAuth();

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

      res += `
VĐV: ${t.athletes.map(a => a.name).join(' & ')}`

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

        {isAdmin && <button className="btn btn-secondary" onClick={() => printToPDF()}>📄 Xuất PDF</button>}

        {isAdmin && <button className="btn btn-secondary" onClick={() => {

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

        }}>📊 Xuất Excel</button>}

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




// ─── APP ROOT ────────────────────────────────────────────────────────────

export default function App() {
  const [categories, setCategories] = useState<Category[]>([])
  const [activeCatId, setActiveCatId] = useState<number | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('teams')
  const [isAdmin, setIsAdmin] = useState(() => localStorage.getItem('isAdmin') === 'true')
  const [showLogin, setShowLogin] = useState(false)
  const [password, setPassword] = useState('')

  const handleLogin = () => {
    axios.post(`${API}/verify_admin`, { password }).then(res => {
      if(res.data.success) {
        localStorage.setItem('isAdmin', 'true'); setIsAdmin(true); setShowLogin(false);
      } else {
        alert("Sai mật khẩu");
      }
    }).catch(err => {
      alert("Lỗi kết nối tới Server: " + (err.response?.data?.detail || err.message));
    })
  }

  const handleLogout = () => { localStorage.removeItem('isAdmin'); setIsAdmin(false); }

  const [loading, setLoading] = useState(true)
  const { toast, show } = useToast()
  
  
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

  const handleInitialReload = () => {
    setLoading(true)
    axios.post(`${API}/reload_teams`)
      .then(r => { show(r.data.message); fetchData() })
      .catch(() => show('Lỗi kết nối hoặc lỗi dữ liệu', 'error'))
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

  const tabs: { id: TabType; label: string; icon: string; adminOnly?: boolean }[] = [
    { id: 'teams',    label: 'Danh sách đội',  icon: '👥', adminOnly: true },
    { id: 'draw',     label: 'Bốc thăm',      icon: '🎲' },
    { id: 'schedule', label: 'Lịch thi đấu',   icon: '📅' },
    { id: 'results',  label: 'Kết quả',       icon: '📊' },
    { id: 'search',   label: 'Tra cứu đa năng', icon: '🔍' }
  ]

  const catIcon = (c: Category) => c.sport === 'Bóng đá' ? '⚽' : '🏓'

  return (
    <AuthContext.Provider value={{ isAdmin }}><div className="app-layout">
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
          {!isAdmin ? <button className="btn btn-ghost" style={{color:"white", borderColor:"rgba(255,255,255,0.5)"}} onClick={()=>setShowLogin(true)}>🔒 Admin Login</button> : <button className="btn btn-ghost" style={{color:"white", borderColor:"rgba(255,255,255,0.5)"}} onClick={handleLogout}>🔓 Thoát Admin</button>}
        <img src="/logo_mt_03.png" alt="Sponsor Logo" style={{ height: 48, objectFit: 'contain' }} />
      </header>

      {/* ── Nav Tabs ── */}
      <nav className="app-nav">
        {tabs.filter(t => isAdmin || !t.adminOnly).map(tab => (
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
                 <label className="btn btn-primary" style={{cursor: 'pointer', display: 'inline-block'}}>
                   {loading ? "⏳ Đang xử lý..." : "🔄 Tải lên file Excel DATA"}
                   <input type="file" accept=".xlsx" style={{display: 'none'}} onChange={handleFileUpload} disabled={loading} />
                 </label>
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
    {showLogin && <div style={{position: "fixed", top:0, left:0, right:0, bottom:0, background: "rgba(0,0,0,0.5)", zIndex: 9999, display: "flex", alignItems: "center", justifyContent: "center"}}><div style={{background: "white", padding: 30, borderRadius: 12, textAlign: "center"}}><h2>Đăng nhập Admin</h2><input type="password" value={password} onChange={e=>setPassword(e.target.value)} style={{padding: 10, margin: "20px 0", width: "100%", fontSize: 18}}/><br/><button className="btn btn-primary" onClick={handleLogin}>Đăng nhập</button> <button className="btn btn-ghost" onClick={()=>setShowLogin(false)}>Hủy</button></div></div>}
    </AuthContext.Provider>
  )
}
