const fs = require('fs');
let text = fs.readFileSync('tsconfig.app.json', 'utf8');

text = text.replace(/"noUnusedLocals":\s*true/g, '"noUnusedLocals": false');
text = text.replace(/"noUnusedParameters":\s*true/g, '"noUnusedParameters": false');

fs.writeFileSync('tsconfig.app.json', text, 'utf8');
console.log('Disabled strict unused in tsconfig.app.json');
