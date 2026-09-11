import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

const API = import.meta.env.PROD ? '/api' : `http://${window.location.hostname}:8000`

export default function LedScreen() {
  const [ledState, setLedState] = useState<any>(null)
  const [categories, setCategories] = useState<any[]>([])
  const [teams, setTeams] = useState<any[]>([])
  const [slots, setSlots] = useState<any[]>([])
  const [matches, setMatches] = useState<any[]>([])
  
  useEffect(() => {
    axios.get(API + '/categories').then(res => setCategories(res.data)).catch(console.error)
    
    const fetchLed = () => {
      axios.get(API + '/led_state').then(res => setLedState(res.data)).catch(console.error)
    }
    fetchLed()
    const interval = setInterval(fetchLed, 1000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (!ledState || ledState.type === 'none') return;
    const cid = ledState.data?.categoryId || ledState.data?.category?.id;
    if (!cid) return;

    const fetchRealtime = () => {
      axios.get(`${API}/categories/${cid}/teams`).then(res => setTeams(res.data)).catch(console.error)
      if (ledState.type === 'all_brackets' || ledState.type === 'bracket') {
         axios.get(`${API}/categories/${cid}/bracket_slots`).then(res => setSlots(res.data)).catch(console.error)
      } else if (ledState.type === 'schedule') {
         axios.get(`${API}/categories/${cid}/matches`).then(res => setMatches(res.data)).catch(console.error)
      }
    }
    
    fetchRealtime();
    const interval = setInterval(fetchRealtime, 1000);
    return () => clearInterval(interval);
  }, [ledState?.type, ledState?.data?.categoryId, ledState?.data?.category?.id])

  if (!ledState || ledState.type === 'none') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#001529', color: 'white', alignItems: 'center', justifyContent: 'center' }}>
        <img src="/logo_daihoi.png" alt="Logo" style={{ height: 180, marginBottom: 20 }} />
        <h1 style={{ fontSize: 48, fontWeight: 'bold', textAlign: 'center', margin: 0 }}>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
      </div>
    )
  }

  const cid = ledState.data?.categoryId || ledState.data?.category?.id;
  const category = categories.find(c => c.id === cid) || ledState.data?.category;

    const orderedSlots = slots.slice().sort((a: any, b: any) => {
    if (a.match_number !== b.match_number) return a.match_number - b.match_number;
    return a.position_in_match - b.position_in_match;
  });
  const getGlobalSlotNum = (slotId: number) => {
    const idx = orderedSlots.findIndex((s: any) => s.id === slotId);
    return idx >= 0 ? idx + 1 : 0;
  };

  if (ledState.type === 'all_brackets') {
    const { isFootball } = ledState.data
    if (!slots.length && !teams.length) return <div style={{padding: 40}}>Loading brackets...</div>

    const populatedSlots = slots.map((s:any) => ({...s, team: teams.find((t:any) => t.id === s.team_id)}))

    const matchGroups: Record<number, any[]> = {}
    for (const s of populatedSlots) {
      if (!matchGroups[s.match_number]) matchGroups[s.match_number] = []
      matchGroups[s.match_number].push(s)
    }
    
    const entries = Object.entries(matchGroups)

    return (
    <div style={{ background: '#f5f6fa', minHeight: '100vh' }}>

      <header className="app-header">
        <div className="header-logo-area">
          <img src="/logo_daihoi.png" alt="Logo Đại hội" style={{ height: 48, objectFit: 'contain' }} />
          <div className="header-title">
            <h1 style={{margin: 0}}>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
            <small>Bóng đá Nam · Pickleball · Khu liên hợp thể thao Thanh Hà, Hà Nội</small>
          </div>
        </div>
        <div className="header-spacer" style={{flex: 1}} />
        <img src="/logo_mt_03.png" alt="Sponsor Logo" style={{ height: 48, objectFit: 'contain' }} />
      </header>

      <div style={{ padding: '20px 40px' }}>
        <h1 style={{ textAlign: 'center', fontSize: 40, color: '#c0392b', marginBottom: 30, textTransform: 'uppercase' }}>
          {category?.name || 'Sơ đồ thi đấu'}
        </h1>
        <div className="bracket-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))' }}>
          {entries.map(([matchNum, slotList]) => {
            const sorted = [...slotList].sort((a:any, b:any) => a.position_in_match - b.position_in_match)
            const code = sorted[0]?.label || sorted[0]?.slot_code || `Trận ${matchNum}`
            const bothAssigned = sorted.every((s:any) => s.team_id)
            
            return (
              <div className={`match-card ${bothAssigned ? 'match-card-complete' : ''}`} key={matchNum}>
                <div className={`match-header ${isFootball ? 'football' : 'pickleball'}`}>
                  <span>{isFootball ? '⚽' : '🏓'} {code}</span>
                  <span style={{ fontSize: 11, opacity: 0.85 }}>{bothAssigned ? '✅ Đủ đội' : `${sorted.filter((s:any) => s.team_id).length}/${sorted.length} đội`}</span>
                </div>
                {sorted.map((slot: any, idx: number) => {
                  const isAssigned = !!slot.team_id;
                  return (
                    <div key={slot.id} className={`match-slot ${isAssigned ? 'slot-assigned' : ''}`}>
                      <div className="slot-position" style={{display: 'flex', flexDirection: 'column'}}>
                        <span>Đội {idx + 1}</span>
                        <span style={{color: '#d32f2f', fontWeight: 'bold', fontSize: '1.1rem', marginTop: 12, marginBottom: 12}}>
                          Số {getGlobalSlotNum(slot.id).toString().padStart(2, '0')}
                        </span>
                      </div>
                      <span className={`slot-code-badge ${isAssigned ? 'badge-assigned' : 'badge-empty'}`}>
                        {slot.team?.draw_code || (isAssigned ? '✓' : '—')}
                      </span>
                      <div className="slot-select" style={{ cursor: 'default', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {slot.team ? ((slot.team.draw_code && slot.team.draw_code !== slot.team.name ? `[${slot.team.draw_code}] ` : '') + slot.team.name) : '-- Chưa bốc thăm --'}
                      </div>
                      {isAssigned && slot.team && slot.team.athletes?.length > 0 && (
                        <div className="slot-athletes">
                          VĐV: {slot.team.athletes.map((a:any)=>a.name).join(' & ')}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )
          })}
        </div>
      </div>
    </div>
    )
  }

  if (ledState.type === 'bracket') {
    const { matchNum, isFootball, slotList } = ledState.data
    const currentSlots = slots.length > 0 ? slots : slotList;
    if (!currentSlots) return <div style={{padding: 40}}>Loading match...</div>

    const latestSlots = currentSlots.map((s:any) => {
        return { ...s, team: teams.find((t:any) => t.id === s.team_id) || s.team }
    })
    
    // The admin projected a specific match_number.
    const sorted = [...latestSlots].filter(s => s.match_number == matchNum).sort((a: any, b: any) => a.position_in_match - b.position_in_match)
    const renderSlots = sorted.length > 0 ? sorted : [...latestSlots].sort((a: any, b: any) => a.position_in_match - b.position_in_match);

    const code = renderSlots[0]?.label || renderSlots[0]?.slot_code || "Trận " + matchNum
    const groupName = "Bảng " + matchNum
    const bothAssigned = renderSlots.every((s:any) => s.team_id)

    return (
    <div style={{ background: '#f5f6fa', minHeight: '100vh' }}>

      <header className="app-header">
        <div className="header-logo-area">
          <img src="/logo_daihoi.png" alt="Logo Đại hội" style={{ height: 48, objectFit: 'contain' }} />
          <div className="header-title">
            <h1 style={{margin: 0}}>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
            <small>Bóng đá Nam · Pickleball · Khu liên hợp thể thao Thanh Hà, Hà Nội</small>
          </div>
        </div>
        <div className="header-spacer" style={{flex: 1}} />
        <img src="/logo_mt_03.png" alt="Sponsor Logo" style={{ height: 48, objectFit: 'contain' }} />
      </header>

      <div style={{ padding: '20px 40px' }}>
        <h1 style={{ textAlign: 'center', fontSize: 40, color: '#c0392b', marginBottom: 30, textTransform: 'uppercase' }}>
          {category?.name || 'Sơ đồ thi đấu'}
        </h1>
        <div className="bracket-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))' }}>
          <div className={`match-card ${bothAssigned ? 'match-card-complete' : ''}`} style={{ transform: 'scale(1.2)', transformOrigin: 'top center', margin: '0 auto' }}>
            <div className={`match-header ${isFootball ? 'football' : 'pickleball'}`}>
              <span>{isFootball ? '⚽' : '🏓'} {code}</span>
              <span style={{ fontSize: 11, opacity: 0.85 }}>{bothAssigned ? '✅ Đủ đội' : `${renderSlots.filter((s:any) => s.team_id).length}/${renderSlots.length} đội`}</span>
            </div>
            {renderSlots.map((slot: any, idx: number) => {
              const isAssigned = !!slot.team_id;
              return (
                <div key={slot.id} className={`match-slot ${isAssigned ? 'slot-assigned' : ''}`}>
                  <div className="slot-position" style={{display: 'flex', flexDirection: 'column'}}>
                        <span>Đội {idx + 1}</span>
                        <span style={{color: '#d32f2f', fontWeight: 'bold', fontSize: '1.1rem', marginTop: 12, marginBottom: 12}}>
                          Số {getGlobalSlotNum(slot.id).toString().padStart(2, '0')}
                        </span>
                      </div>
                  <span className={`slot-code-badge ${isAssigned ? 'badge-assigned' : 'badge-empty'}`}>
                    {slot.team?.draw_code || (isAssigned ? '✓' : '—')}
                  </span>
                  <div className="slot-select" style={{ cursor: 'default', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {slot.team ? ((slot.team.draw_code && slot.team.draw_code !== slot.team.name ? `[${slot.team.draw_code}] ` : '') + slot.team.name) : '-- Chưa bốc thăm --'}
                  </div>
                  {isAssigned && slot.team && slot.team.athletes?.length > 0 && (
                    <div className="slot-athletes">
                      VĐV: {slot.team.athletes.map((a:any)=>a.name).join(' & ')}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
    )
  }

  if (ledState.type === 'schedule') {
    const { date, isFootball } = ledState.data
    const dateMatches = matches.length > 0 ? matches.filter(m => {
        const d = new Date(m.scheduled_time || '');
        const dStr = !isNaN(d.getTime()) ? d.toLocaleDateString('vi-VN') : '';
        return dStr === date || m.scheduled_time?.includes(date) || ledState.data.matches?.find((om:any)=>om.id === m.id);
    }) : ledState.data.matches;

    const latestMatches = (dateMatches || []).map((m:any) => {
        const team1 = teams.find((t:any) => t.id === m.team1_id) || m.team1;
        const team2 = teams.find((t:any) => t.id === m.team2_id) || m.team2;
        return { ...m, team1, team2 }
    })
    
    return (
    <div style={{ background: '#f0f2f5', minHeight: '100vh', overflowY: 'auto' }}>

      <header className="app-header">
        <div className="header-logo-area">
          <img src="/logo_daihoi.png" alt="Logo Đại hội" style={{ height: 48, objectFit: 'contain' }} />
          <div className="header-title">
            <h1 style={{margin: 0}}>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
            <small>Bóng đá Nam · Pickleball · Khu liên hợp thể thao Thanh Hà, Hà Nội</small>
          </div>
        </div>
        <div className="header-spacer" style={{flex: 1}} />
        <img src="/logo_mt_03.png" alt="Sponsor Logo" style={{ height: 48, objectFit: 'contain' }} />
      </header>

      <div style={{ padding: 40 }}>
        <h1 style={{ textAlign: 'center', fontSize: 48, color: '#C62828', marginBottom: 10 }}>{category?.name}</h1>
        <h2 style={{ textAlign: 'center', fontSize: 36, color: '#1565C0', marginBottom: 40 }}>LỊCH THI ĐẤU - {date}</h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 1200, margin: '0 auto' }}>
          {latestMatches.map((m: any) => (
            <div key={m.id} style={{ 
              background: 'white', borderRadius: 16, padding: '24px 32px',
              boxShadow: '0 8px 32px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center', gap: 24
            }}>
              <div style={{ fontSize: 32, fontWeight: 'bold', color: '#1565C0', minWidth: 120 }}>{m.scheduled_time || '--:--'}</div>
              <div style={{ fontSize: 24, background: '#E3F2FD', color: '#003c8f', padding: '6px 16px', borderRadius: 8, minWidth: 100, textAlign: 'center' }}>
                {m.court || 'Sân ?'}
              </div>
              <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 32 }}>
                <div style={{ flex: 1, textAlign: 'right', fontSize: 32, fontWeight: 'bold' }}>{m.team1?.name || '---'}</div>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#EF5350' }}>VS</div>
                <div style={{ flex: 1, textAlign: 'left', fontSize: 32, fontWeight: 'bold' }}>{m.team2?.name || '---'}</div>
              </div>
              <div style={{ fontSize: 20, color: '#757575', minWidth: 100, textAlign: 'center' }}>Trận {m.match_code}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
    )
  }

  return (
    <div style={{ padding: 40, background: '#f0f2f5', height: '100vh' }}>
      <h1>Đang hiển thị...</h1>
    </div>
  )
}
