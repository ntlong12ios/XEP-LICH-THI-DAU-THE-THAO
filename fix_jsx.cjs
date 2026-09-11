const fs = require('fs');
let text = fs.readFileSync('frontend/src/App.tsx', 'utf8');

text = text.replace(
    /\{isAssigned && \(\s*\{isAdmin && <button className="btn-unassign"/g,
    `{isAssigned && isAdmin && (<button className="btn-unassign"`
);
// Also let's check the closing tag
text = text.replace(
    /onClick=\{\(\) => assignTeam\(slot\.id, null\)\}>✖<\/button>\}\s*\)\}/g,
    `onClick={() => assignTeam(slot.id, null)}>✖</button>\n                      )}`
);

fs.writeFileSync('frontend/src/App.tsx', text, 'utf8');
console.log('Fixed JSX syntax error');
