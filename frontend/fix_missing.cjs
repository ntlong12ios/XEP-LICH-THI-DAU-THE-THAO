const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// Add to DrawScreen
text = text.replace(/function DrawScreen\({.*?}\)\s*{/, (m) => {
    return m + '\n  const { isAdmin } = useAuth();';
});

// Add to GlobalSearchScreen
text = text.replace(/function GlobalSearchScreen\({.*?}\)\s*{/, (m) => {
    return m + '\n  const { isAdmin } = useAuth();';
});

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed missing useAuth injections');
