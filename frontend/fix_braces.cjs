const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// The closing brace is missing for generateBracket
text = text.replace(/{isAdmin && <button className="btn btn-primary" onClick={generateBracket} disabled={loading}>[\s\S]*?<\/button>/, (m) => m + '}');

// The closing brace is missing for exportToExcel in DrawScreen
text = text.replace(/{isAdmin && <button className="btn btn-secondary" onClick={\(\) => {[\s\S]*?BocTham_[\s\S]*?<\/button>/, (m) => m + '}');

// The closing brace is missing for generateSchedule
text = text.replace(/{isAdmin && <button className="btn btn-primary" onClick={generateSchedule} disabled={loading}>[\s\S]*?<\/button>/, (m) => m + '}');

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed');
