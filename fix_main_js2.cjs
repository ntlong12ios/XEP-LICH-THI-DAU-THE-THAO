const fs = require('fs');
let text = fs.readFileSync('backend/main.py', 'utf8');

text = text.replace(/B\?ng/g, 'Bảng');
text = text.replace(/D\?i/g, 'Đội');
text = text.replace(/B\? Nam/g, 'BĐ Nam');
text = text.replace(/B\?ng d\?/g, 'Bóng đá');
text = text.replace(/Tr\?n R1-/g, 'Trận R1-');
text = text.replace(/Bng d/g, 'Bóng đá');
text = text.replace(/Trn/g, 'Trận');

fs.writeFileSync('backend/main.py', text, 'utf8');
console.log('Fixed main.py strings using literal replacement!');
