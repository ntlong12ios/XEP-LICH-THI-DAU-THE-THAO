const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

const injection = `
import { createContext, useContext } from 'react';

export const AuthContext = createContext({ isAdmin: false });
export const useAuth = () => useContext(AuthContext);

const projectToLed = (type, data) => {
    axios.post('http://' + window.location.hostname + ':8000/led_state', { type, data })
         .then(() => alert("Đã chuyển tín hiệu lên màn LED"))
         .catch(() => alert("Lỗi kết nối màn LED"))
};
`;

if (!text.includes('AuthContext')) {
    text = text.replace("import axios from 'axios'", "import axios from 'axios'\n" + injection);
}

// In DrawScreen, it complains about `isAdmin` not found, meaning `const { isAdmin } = useAuth()` was NOT added to DrawScreen!
if (!text.includes('const { isAdmin } = useAuth()', text.indexOf('function DrawScreen'))) {
    text = text.replace('function DrawScreen({ category, teams, onRefresh }: {', 'function DrawScreen({ category, teams, onRefresh }: {\n  const { isAdmin } = useAuth();');
}

// Fix DrawScreen bracket/braces syntax error if any, wait, it says `Cannot find name 'isAdmin'` at line 295.
// Let's just blindly inject it if it's missing inside DrawScreen.
text = text.replace(/function DrawScreen\([^)]*\)\s*{[\s\S]*?(?=const \[slots)/, (m) => {
    if (!m.includes('useAuth')) {
        return m + '\n  const { isAdmin } = useAuth();\n';
    }
    return m;
});


fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed missing imports');
