const fs = require('fs');
let text = fs.readFileSync('backend/main.py', 'utf8');
const lines = text.split('\n');
const line = lines.find(l => l.includes('slot_code=f"B'));
console.log(line);
for(let i=0; i<line.length; i++) {
  console.log(line[i], line.charCodeAt(i).toString(16));
}
