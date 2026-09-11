const fs = require('fs');
const text = fs.readFileSync('backend/main.py', 'utf8');
const lines = text.split('\n');
lines.forEach((line, i) => {
    if (line.includes('B') && line.includes('ng')) console.log(`${i+1}: ${line}`);
})
