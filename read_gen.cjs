const fs = require('fs');
const text = fs.readFileSync('backend/bracket_generator.py', 'utf8');
console.log(text.substring(0, 1000));
