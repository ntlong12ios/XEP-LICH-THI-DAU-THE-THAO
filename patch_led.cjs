const fs = require('fs');
let text = fs.readFileSync('frontend/src/LedScreen.tsx', 'utf8');

text = text.replace(
    /const code = sorted\[0\]\?\.slot_code \|\| `Trận \$\{matchNum\}`/g,
    'const code = sorted[0]?.label || sorted[0]?.slot_code || `Trận ${matchNum}`'
);
text = text.replace(
    /const code = renderSlots\[0\]\?\.slot_code \|\| "Trận " \+ matchNum/g,
    'const code = renderSlots[0]?.label || renderSlots[0]?.slot_code || "Trận " + matchNum'
);

fs.writeFileSync('frontend/src/LedScreen.tsx', text, 'utf8');
console.log('Patched LedScreen.tsx');
