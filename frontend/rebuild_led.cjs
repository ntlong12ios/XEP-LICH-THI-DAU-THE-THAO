const fs = require('fs');
const content = `import { useEffect, useState } from 'react'
import axios from 'axios'

const API = 'http://' + window.location.hostname + ':8000'

export default function LedScreen() {
  const [ledState, setLedState] = useState<any>(null)
  
  useEffect(() => {
    const interval = setInterval(() => {
      axios.get(API + '/led_state')
        .then(res => setLedState(res.data))
        .catch(err => console.error(err))
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  if (!ledState || ledState.type === 'none') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#001529', color: 'white', alignItems: 'center', justifyContent: 'center' }}>
        <img src="/logo_daihoi.png" alt="Logo" style={{ height: 180, marginBottom: 20 }} />
        <h1 style={{ fontSize: 48, fontWeight: 'bold', textAlign: 'center', margin: 0 }}>GIẢI THỂ THAO MƯỜNG THANH MỞ RỘNG 2026</h1>
      </div>
    )
  }

  if (ledState.type === 'bracket') {
    const { matchNum, slotList, category } = ledState.data
    const sorted = [...slotList].sort((a: any, b: any) => a.position_in_match - b.position_in_match)
    const code = sorted[0]?.slot_code || "Trận " + matchNum
    const groupName = "Bảng " + matchNum

    return (
      <div style={{ padding: 40, background: '#f0f2f5', minHeight: '100vh', overflowY: 'auto' }}>
        <h1 style={{ textAlign: 'center', fontSize: 48, color: '#C62828', marginBottom: 10 }}>{category?.name}</h1>
        <h2 style={{ textAlign: 'center', fontSize: 36, color: '#1565C0', marginBottom: 40 }}>{groupName} - {code}</h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24, maxWidth: 1000, margin: '0 auto' }}>
          {sorted.map((slot: any, pos: number) => {
            const isAssigned = !!slot.team_id
            return (
              <div key={slot.id} style={{ 
                background: 'white', borderRadius: 16, padding: '24px 32px',
                boxShadow: '0 8px 32px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center', gap: 24
              }}>
                <div style={{ fontSize: 28, fontWeight: 'bold', color: '#757575', minWidth: 100 }}>{pos === 0 ? 'Đội 1' : 'Đội 2'}</div>
                <div style={{ 
                  background: isAssigned ? '#E0F2F1' : '#FFF3E0', color: isAssigned ? '#00897B' : '#E65100',
                  padding: '8px 24px', borderRadius: 12, fontSize: 24, fontWeight: 'bold'
                }}>
                  Mã: {slot.team?.draw_code || 'Chưa có'}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 36, fontWeight: 'bold', color: isAssigned ? '#212121' : '#9E9E9E' }}>
                    {slot.team ? slot.team.name : '--- Chưa bốc thăm ---'}
                  </div>
                  {isAssigned && slot.team?.athletes?.length > 0 && (
                    <div style={{ fontSize: 20, color: '#1565C0', marginTop: 8 }}>
                      VĐV: {slot.team.athletes.map((a: any) => a.name).join(' & ')}
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  if (ledState.type === 'schedule') {
    const { date, matches, category } = ledState.data
    return (
      <div style={{ padding: 40, background: '#f0f2f5', minHeight: '100vh', overflowY: 'auto' }}>
        <h1 style={{ textAlign: 'center', fontSize: 48, color: '#C62828', marginBottom: 10 }}>{category?.name}</h1>
        <h2 style={{ textAlign: 'center', fontSize: 36, color: '#1565C0', marginBottom: 40 }}>LỊCH THI ĐẤU - {date}</h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 1200, margin: '0 auto' }}>
          {matches.map((m: any) => (
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
    )
  }

  return (
    <div style={{ padding: 40, background: '#f0f2f5', height: '100vh' }}>
      <h1>Đang hiển thị...</h1>
    </div>
  )
}
`;
fs.writeFileSync('src/LedScreen.tsx', content, 'utf8');
console.log('LedScreen rebuilt');
