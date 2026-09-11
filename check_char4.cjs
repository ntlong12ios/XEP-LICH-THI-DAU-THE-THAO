const fs = require('fs');
let text = fs.readFileSync('backend/bracket_generator.py', 'utf8');
const lines = text.split('\n');
const line = lines.find(l => l.includes('T') && l.includes('k'));
console.log(line);
for(let i=0; i<line.length; i++) {
  if (line[i].trim()) console.log(line[i], line.charCodeAt(i).toString(16));
}
