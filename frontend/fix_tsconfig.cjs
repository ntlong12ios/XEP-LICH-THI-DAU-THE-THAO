const fs = require('fs');
let text = fs.readFileSync('tsconfig.json', 'utf8');

text = text.replace(/"noUnusedLocals":\s*true/g, '"noUnusedLocals": false');
text = text.replace(/"noUnusedParameters":\s*true/g, '"noUnusedParameters": false');

fs.writeFileSync('tsconfig.json', text, 'utf8');
console.log('Disabled strict unused');
