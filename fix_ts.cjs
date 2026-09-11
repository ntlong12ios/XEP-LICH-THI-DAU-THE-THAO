const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');

text = text.replace(
    /const tabs: \{ id: TabType; label: string; icon: string \}\[\] = \[/g,
    `const tabs: { id: TabType; label: string; icon: string; adminOnly?: boolean }[] = [`
);

fs.writeFileSync('frontend/src/App.tsx', text, 'utf8');
console.log('Fixed TS type error');
