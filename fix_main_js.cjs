const fs = require('fs');
let text = fs.readFileSync('backend/main.py', 'utf8');

// Replace using regex to be completely safe from weird characters
text = text.replace(/f"B.*?ng \{g_name\} - .*? \{pos\}"/g, 'f"Bảng {g_name} - Đội {pos}"');
text = text.replace(/f"B.*?ng \{i\+1\}"/g, 'f"Bảng {i+1}"');
text = text.replace(/label=f"B.*?ng \{g_name\}"/g, 'label=f"Bảng {g_name}"');
text = text.replace(/"B.*?ng d.*?"/g, '"Bóng đá"');
text = text.replace(/"Tr.*?n R1-"/g, '"Trận R1-"');
text = text.replace(/"B.*? Nam "/g, '"BĐ Nam "');

fs.writeFileSync('backend/main.py', text, 'utf8');
console.log('Fixed main.py strings using JS!');
