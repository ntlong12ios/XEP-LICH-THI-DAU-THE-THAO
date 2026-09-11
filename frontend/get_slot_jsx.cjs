const fs = require('fs');
const text = fs.readFileSync('src/App.tsx', 'utf8');

const start = text.indexOf('const sorted = [...slotList].sort(');
const end = text.indexOf('return (', start + 1000) > -1 ? text.indexOf('return (', start + 1000) : start + 3000;
console.log(text.substring(start, start + 3000));
