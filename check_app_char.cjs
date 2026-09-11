const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');
const lines = text.split('\n');
const line = lines.find(l => l.includes('const isFootball'));
console.log(line);
for(let i=0; i<line.length; i++) {
  if (line[i].trim()) console.log(line[i], line.charCodeAt(i).toString(16));
}
