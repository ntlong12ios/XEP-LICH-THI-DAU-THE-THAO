const fs = require('fs');
const text = fs.readFileSync('src/App.tsx', 'utf8');

const start = text.indexOf(' {/* Unassign button */}');
const end = start + 2000;
console.log(text.substring(start, end));
