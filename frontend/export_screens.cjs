const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

text = text.replace('function DrawScreen', 'export function DrawScreen');
text = text.replace('function ScheduleScreen', 'export function ScheduleScreen');
text = text.replace('function ResultsScreen', 'export function ResultsScreen');

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Exported screens');
