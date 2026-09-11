import sys, re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if 'exportUtils' not in content:
    content = content.replace(\"import axios from 'axios'\", \"import axios from 'axios'\nimport { exportToExcel, printToPDF } from './utils/exportUtils'\")

# TeamsScreen
teams_export = '''
        <button className=\"btn\" onClick={() => printToPDF()}><span className=\"btn-icon\">??</span> Xu?t PDF</button>
        <button className=\"btn\" onClick={() => {
            const data = filteredTeams.map((t, i) => ({
              'STT': i + 1,
              'Mã d?i': t.draw_code || '',
              'Tên d?i': t.name,
              'V?n d?ng viên': t.athletes?.map(a => a.name).join(', ') || '',
              'Liên h?': t.contact_name || '',
              'SÐT': t.contact_phone || ''
            }));
            exportToExcel(data, \DanhSachDoi_\\);
        }}><span className=\"btn-icon\">??</span> Xu?t Excel</button>
'''
content = content.replace(
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm tên d?i ho?c v?n d?ng viên...\" value={search} onChange={e => setSearch(e.target.value)} />',
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm tên d?i ho?c v?n d?ng viên...\" value={search} onChange={e => setSearch(e.target.value)} />' + teams_export
)

# DrawScreen
draw_export = '''
        <button className=\"btn\" onClick={() => printToPDF()}><span className=\"btn-icon\">??</span> Xu?t PDF</button>
        <button className=\"btn\" onClick={() => {
            const data = filteredEntries.map(([matchNum, slots]) => {
                const groupName = \B?ng \\;
                return slots.map(s => ({
                    'B?ng': groupName,
                    'V? trí': s.position_in_match,
                    'Mã b?c tham': s.slot_code,
                    'Tên d?i': s.team ? s.team.name : '---'
                }));
            }).flat();
            exportToExcel(data, \BocTham_\\);
        }}><span className=\"btn-icon\">??</span> Xu?t Excel</button>
'''
content = content.replace(
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm mã b?c tham ho?c tên d?i...\" value={search} onChange={e => setSearch(e.target.value)} />',
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm mã b?c tham ho?c tên d?i...\" value={search} onChange={e => setSearch(e.target.value)} />' + draw_export
)

# ScheduleScreen
schedule_export = '''
          <button className=\"btn\" onClick={() => printToPDF()}><span className=\"btn-icon\">??</span> Xu?t PDF</button>
          <button className=\"btn\" onClick={() => {
              const data = matches.map((m, i) => ({
                  'STT': i + 1,
                  'Gi?': m.scheduled_time || '',
                  'Sân': m.court || '',
                  'Tr?n': m.match_code,
                  'Ð?i 1': m.team1 ? m.team1.name : '?',
                  'Ð?i 2': m.team2 ? m.team2.name : '?'
              }));
              exportToExcel(data, \LichThiDau_\\);
          }}><span className=\"btn-icon\">??</span> Xu?t Excel</button>
'''
content = content.replace(
    '<button className=\"btn btn-primary\" onClick={generateMatches} disabled={genLoading}>',
    schedule_export + '\n          <button className=\"btn btn-primary\" onClick={generateMatches} disabled={genLoading}>'
)

# ResultsScreen
results_export = '''
          <button className=\"btn\" onClick={() => printToPDF()}><span className=\"btn-icon\">??</span> Xu?t PDF</button>
          <button className=\"btn\" onClick={() => {
              const data = matches.map((m, i) => ({
                  'STT': i + 1,
                  'Tr?n': m.match_code,
                  'Ð?i 1': m.team1 ? m.team1.name : '?',
                  'Ði?m 1': m.score_team1 !== null ? m.score_team1 : '',
                  'Ði?m 2': m.score_team2 !== null ? m.score_team2 : '',
                  'Ð?i 2': m.team2 ? m.team2.name : '?',
                  'Tr?ng thái': m.status === 'completed' ? 'Ðã xong' : 'Chua d?u'
              }));
              exportToExcel(data, \KetQua_\\);
          }}><span className=\"btn-icon\">??</span> Xu?t Excel</button>
'''
content = content.replace(
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm d?i bóng, mã tr?n...\" value={search} onChange={e => setSearch(e.target.value)} style={{ minWidth: 200 }} />',
    '<input type=\"text\" className=\"search-input\" placeholder=\"Tìm d?i bóng, mã tr?n...\" value={search} onChange={e => setSearch(e.target.value)} style={{ minWidth: 200 }} />' + results_export
)

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
