const fs = require('fs');
const lines = fs.readFileSync('frontend/src/App.tsx', 'utf8').split('\n');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Nhập kết quả')) {
        console.log(`Line ${i+1}: ${lines[i].trim()}`);
    }
}
