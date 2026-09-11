const fs = require('fs');
let text = fs.readFileSync('backend/import_excel.py', 'utf8');
const lines = text.split('\n');
const line = lines.find(l => l.includes('Tranh') && l.includes('ng'));
console.log(line);
for(let i=0; i<line.length; i++) {
  if (line[i].trim()) console.log(line[i], line.charCodeAt(i).toString(16));
}
