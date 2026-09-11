const fs = require('fs');

let appText = fs.readFileSync('src/App.tsx', 'utf8');
appText = appText.replace(/<div className="slot-position">\{pos === 0 \? 'Đội 1' : 'Đội 2'\}<\/div>/g, '<div className="slot-position">Đội {pos + 1}</div>');
fs.writeFileSync('src/App.tsx', appText, 'utf8');
console.log('Fixed App.tsx slot-position');

let ledText = fs.readFileSync('src/LedScreen.tsx', 'utf8');
ledText = ledText.replace(/<div className="slot-position">\{sorted\[0\]\?\.slot_code\?\.includes\('Trận'\) \? 'Đội' : 'Vị trí'\} \{idx \+ 1\}<\/div>/g, '<div className="slot-position">Đội {idx + 1}</div>');
ledText = ledText.replace(/<div className="slot-position">\{renderSlots\[0\]\?\.slot_code\?\.includes\('Trận'\) \? 'Đội' : 'Vị trí'\} \{idx \+ 1\}<\/div>/g, '<div className="slot-position">Đội {idx + 1}</div>');
fs.writeFileSync('src/LedScreen.tsx', ledText, 'utf8');
console.log('Fixed LedScreen.tsx slot-position');
