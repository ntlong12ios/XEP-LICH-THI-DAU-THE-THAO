const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');

text = text.replace(
    /<button className="btn btn-secondary" onClick=\{loadAgenda\} disabled=\{genLoading\}>/g,
    `{isAdmin && <button className="btn btn-secondary" onClick={loadAgenda} disabled={genLoading}>`
);
text = text.replace(
    /\{genLoading \? '⏳' : '📥'\} Tải Agenda từ Excel\s*<\/button>/g,
    `{genLoading ? '⏳' : '📥'} Tải Agenda từ Excel\n        </button>}`
);

text = text.replace(
    /<button className="btn btn-outline" onClick=\{handlePrint\}>🖨️ In lịch thi đấu<\/button>/g,
    `{isAdmin && <button className="btn btn-outline" onClick={handlePrint}>🖨️ In lịch thi đấu</button>}`
);

fs.writeFileSync('frontend/src/App.tsx', text, 'utf8');
console.log('Patched missing buttons');
