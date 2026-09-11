const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// Revert the broken </select>} first
text = text.replace(/<\/select>}/g, '</select>');

// DrawScreen: select format
text = text.replace('<select className="search-input" style={{ width: 220 }} value={drawFormat} onChange={e => setDrawFormat(e.target.value)}>', '{isAdmin && <select className="search-input" style={{ width: 220 }} value={drawFormat} onChange={e => setDrawFormat(e.target.value)}>');
text = text.replace(/Chia bảng \(Đấu vòng tròn\)<\/option>\s*<\/select>/g, 'Chia bảng (Đấu vòng tròn)</option>\n        </select>}');

// DrawScreen: round_robin inputs
text = text.replace("{drawFormat === 'round_robin' && (", "{isAdmin && drawFormat === 'round_robin' && (");

// DrawScreen: Tạo sơ đồ
text = text.replace('<button className="btn btn-primary" onClick={generateBracket} disabled={loading}>', '{isAdmin && <button className="btn btn-primary" onClick={generateBracket} disabled={loading}>');

// DrawScreen: slot-select
text = text.replace('<select\n\n                        className="slot-select"', '{isAdmin ? <select\n\n                        className="slot-select"');
text = text.replace('</option>\n\n                        ))}\n\n                      </select>', '</option>\n\n                        ))}\n\n                      </select> : <div className="slot-select" style={{background: "transparent", border: "none"}}>{slot.team?.name || "-- Trống --"}</div>}');

// ScheduleScreen: function def
text = text.replace('function ScheduleScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {', 'function ScheduleScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {\n  const { isAdmin } = useAuth();');

// ScheduleScreen: inputs
text = text.replace('<input\n\n                              className="schedule-time-input"', '{!isAdmin ? <span>{m.scheduled_time || "--:--"}</span> : <input\n\n                              className="schedule-time-input"');
text = text.replace('/>\n\n                          ) : (', '/>\n\n                          )} {!isAdmin ? null : !editingId ? (');
text = text.replace('<input\n\n                              className="schedule-court-input"', '{!isAdmin ? <span>{m.court || "Chưa xếp"}</span> : <input\n\n                              className="schedule-court-input"');
text = text.replace('onBlur={() => handleSaveCourt(m.id, editCourt)}\n\n                            />\n\n                          ) : (', 'onBlur={() => handleSaveCourt(m.id, editCourt)}\n\n                            />\n\n                          )} {!isAdmin ? null : !editingCourtId ? (');

// ScheduleScreen: Tạo lịch tự động
text = text.replace('<button className="btn btn-primary" onClick={generateSchedule} disabled={loading}>', '{isAdmin && <button className="btn btn-primary" onClick={generateSchedule} disabled={loading}>');

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('App.tsx fully patched');
