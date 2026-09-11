const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

text = text.replace(/function DrawScreen\([\s\S]*?\)\s*{/, (m) => {
    return m + '\n  const { isAdmin } = useAuth();';
});

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed DrawScreen');
