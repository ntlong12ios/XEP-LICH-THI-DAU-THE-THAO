const fs = require('fs');
let text = fs.readFileSync('src/LedScreen.tsx', 'utf8');

text = text.replace(
    /\{groupName\} - \{code\}/g,
    '{code}'
);

fs.writeFileSync('src/LedScreen.tsx', text, 'utf8');
console.log('Patched LedScreen.tsx single bracket');
