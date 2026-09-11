const fs = require('fs');

let content = fs.readFileSync('src/LedScreen.tsx', 'utf-8');

const headerStr = `
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
`;

content = content.replace(
  /return \(\s*<div style={{ padding: '20px 40px', minHeight: '100vh', background: '#f5f6fa' }}>/g,
  `return (\n    <div style={{ background: '#f5f6fa', minHeight: '100vh' }}>\n${headerStr}\n      <div style={{ padding: '20px 40px' }}>`
);

content = content.replace(
  /<\/div>\n    \)\n  }\n\n  if \(ledState.type === 'schedule'\)/g,
  `</div>\n      </div>\n    )\n  }\n\n  if (ledState.type === 'schedule')`
);

content = content.replace(
  /return \(\s*<div style={{ padding: 40, background: '#f0f2f5', minHeight: '100vh', overflowY: 'auto' }}>/g,
  `return (\n    <div style={{ background: '#f0f2f5', minHeight: '100vh', overflowY: 'auto' }}>\n${headerStr}\n      <div style={{ padding: 40 }}>`
);

content = content.replace(
  /<\/div>\n    \)\n  }\n\n  return \(/g,
  `</div>\n      </div>\n    )\n  }\n\n  return (`
);

fs.writeFileSync('src/LedScreen.tsx', content);
console.log('Fixed LedScreen.tsx');
