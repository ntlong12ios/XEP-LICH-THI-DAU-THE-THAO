const fs = require('fs');
const lines = fs.readFileSync('frontend/src/App.tsx', 'utf8').split('\n');
for (let i = 1165; i < 1170; i++) {
    console.log(`Line ${i+1}: ${lines[i]}`);
}
