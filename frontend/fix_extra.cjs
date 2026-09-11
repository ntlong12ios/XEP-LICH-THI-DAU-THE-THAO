const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

text = text.replace(/<\/button>}}/g, '</button>}');
fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed extra brace');
