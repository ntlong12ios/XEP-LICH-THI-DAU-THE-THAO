const fs = require('fs');
const lines = fs.readFileSync('frontend/src/App.tsx', 'utf8').split('\n');
for (let i = 1565; i < 1580; i++) {
    console.log(`Line ${i+1}: ${lines[i]}`);
}
