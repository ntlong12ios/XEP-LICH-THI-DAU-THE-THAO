const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');

// 1. Hide "Danh sách đội" tab
text = text.replace(
    /\{ id: 'teams',    label: 'Danh sách đội',  icon: '👥' \},/,
    `{ id: 'teams',    label: 'Danh sách đội',  icon: '👥', adminOnly: true },`
);
text = text.replace(
    /\{tabs\.map\(tab => \(/,
    `{tabs.filter(t => isAdmin || !t.adminOnly).map(tab => (`
);

// 2. Hide "x" button in DrawScreen
text = text.replace(
    /<button className="btn-unassign" title="Xóa gán"/g,
    `{isAdmin && <button className="btn-unassign" title="Xóa gán"`
);
text = text.replace(
    /onClick=\{\(\) => assignTeam\(slot\.id, null\)\}>✖<\/button>/g,
    `onClick={() => assignTeam(slot.id, null)}>✖</button>}`
);

// 3. Disable dropdown in DrawScreen (if !isAdmin, show plain text or disable select)
// Wait, currently it's a <select> element. Let's just disable it if !isAdmin.
text = text.replace(
    /<select className="slot-select"/g,
    `<select className="slot-select" disabled={!isAdmin}`
);

// 4. Hide ScheduleScreen action buttons
text = text.replace(
    /<button className="btn btn-primary" onClick=\{generateMatches\} disabled=\{genLoading\}>/g,
    `{isAdmin && <button className="btn btn-primary" onClick={generateMatches} disabled={genLoading}>`
);
text = text.replace(
    /\{genLoading \? '⏳' : '⚡'\} \{matches\.length > 0 \? 'Tạo lại lịch từ sơ đồ' : 'Tạo lịch từ sơ đồ bốc thăm'\}/g,
    `{genLoading ? '⏳' : '⚡'} {matches.length > 0 ? 'Tạo lại lịch từ sơ đồ' : 'Tạo lịch từ sơ đồ bốc thăm'}`
);
text = text.replace(
    /onClick=\{generateMatches\} disabled=\{genLoading\}>\s*\{genLoading \? '⏳' : '⚡'\} \{matches\.length > 0 \? 'Tạo lại lịch từ sơ đồ' : 'Tạo lịch từ sơ đồ bốc thăm'\}\s*<\/button>/,
    `onClick={generateMatches} disabled={genLoading}>\n          {genLoading ? '⏳' : '⚡'} {matches.length > 0 ? 'Tạo lại lịch từ sơ đồ' : 'Tạo lịch từ sơ đồ bốc thăm'}\n        </button>}`
);

text = text.replace(
    /<button className="btn btn-secondary" onClick=\{\(\) => document\.getElementById\('agenda-upload'\)\?\.click\(\)\}>/g,
    `{isAdmin && <button className="btn btn-secondary" onClick={() => document.getElementById('agenda-upload')?.click()}>`
);
text = text.replace(
    /onClick=\{\(\) => document\.getElementById\('agenda-upload'\)\?\.click\(\)\}>📥 Tải agenda từ Excel<\/button>/g,
    `onClick={() => document.getElementById('agenda-upload')?.click()}>📥 Tải agenda từ Excel</button>}`
);
text = text.replace(
    /<button className="btn btn-outline" onClick=\{\(\) => window\.print\(\)\}>/g,
    `{isAdmin && <button className="btn btn-outline" onClick={() => window.print()}>`
);
text = text.replace(
    /onClick=\{\(\) => window\.print\(\)\}>🖨️ In lịch thi đấu<\/button>/g,
    `onClick={() => window.print()}>🖨️ In lịch thi đấu</button>}`
);

// 5. Hide edit/pencil icon in ScheduleScreen
text = text.replace(
    /<button className="btn btn-ghost btn-sm" onClick=\{\(\) => setEditId\(match\.id\)\}>✏️<\/button>/g,
    `{isAdmin && <button className="btn btn-ghost btn-sm" onClick={() => setEditId(match.id)}>✏️</button>}`
);

// 6. Hide edit buttons in ResultsScreen
text = text.replace(
    /<button className="btn btn-outline btn-sm" onClick=\{\(\) => startEdit\(match\)\}>/g,
    `{isAdmin && <button className="btn btn-outline btn-sm" onClick={() => startEdit(match)}>`
);
text = text.replace(
    /\{isCompleted \? '✏️ Sửa kết quả' : '📝 Nhập kết quả'\}\s*<\/button>/g,
    `{isCompleted ? '✏️ Sửa kết quả' : '📝 Nhập kết quả'}\n                        </button>}`
);

fs.writeFileSync('frontend/src/App.tsx', text, 'utf8');
console.log('Patched App.tsx for remaining admin controls!');
