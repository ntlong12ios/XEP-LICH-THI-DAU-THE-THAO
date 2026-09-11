const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// Fix Cập nhật thông tin đội
text = text.replace(/Cập nhật thông tin đội\s*<\/button>/g, 'Cập nhật thông tin đội\n        </button>}');

// Fix Tạo sơ đồ bốc thăm
text = text.replace(/Tạo sơ đồ bốc thăm'\s*<\/button>/g, "Tạo sơ đồ bốc thăm'\n        </button>}");

// Fix Tạo lịch tự động
text = text.replace(/Tạo lịch tự động'\s*<\/button>/g, "Tạo lịch tự động'\n        </button>}");

// Fix option round robin
text = text.replace(/Chia bảng \(Đấu vòng tròn\)\s*<\/option>\s*<\/select>/g, "Chia bảng (Đấu vòng tròn)</option>\n        </select>}");


fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed closing tags');
