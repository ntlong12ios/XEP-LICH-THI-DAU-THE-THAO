const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// Use regex to remove duplicate lines of `const { isAdmin } = useAuth();`
text = text.replace(/(const\s*{\s*isAdmin\s*}\s*=\s*useAuth\(\);\s*)+/g, 'const { isAdmin } = useAuth();\n  ');

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed double declarations');
