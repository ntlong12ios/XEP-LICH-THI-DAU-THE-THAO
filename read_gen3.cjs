const fs = require('fs');
const text = fs.readFileSync('backend/bracket_generator.py', 'utf8');
const lines = text.split('\n');
lines.forEach((line, i) => {
    if (line.includes('Bảng')) console.log(`${i+1}: ${line}`);
})
