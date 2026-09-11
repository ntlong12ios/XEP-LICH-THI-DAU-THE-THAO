const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// Fix literal \n
text = text.replace(/\\n/g, '\n');

// Fix missing backticks in axios
text = text.replace('axios.post(${API}/verify_admin', 'axios.post(`${API}/verify_admin`');

// Fix {isAdmin && ... Xuất Excel
// Actually, let's see if we have closing brackets missing.
// I will just do a regex replace to ensure the button is closed properly
text = text.replace(/}}>📊 Xuất Excel<\/button>}/g, '}}>📊 Xuất Excel</button>}');
text = text.replace(/}}>📊 Xuất Excel<\/button>(?!})/g, '}}>📊 Xuất Excel</button>}');

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed');
