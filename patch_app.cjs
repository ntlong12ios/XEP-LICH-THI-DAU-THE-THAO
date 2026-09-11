const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');

text = text.replace(
    /const code = sorted\[0\]\?\.slot_code \|\| `Trận \$\{matchNum\}`/g,
    'const code = sorted[0]?.label || sorted[0]?.slot_code || `Trận ${matchNum}`'
);

fs.writeFileSync('frontend/src/App.tsx', text, 'utf8');
console.log('Patched App.tsx');
