const fs = require('fs');
let lines = fs.readFileSync('src/App.tsx', 'utf8').split('\n');

const injection = `
import { createContext, useContext } from 'react';

export const AuthContext = createContext({ isAdmin: false });
export const useAuth = () => useContext(AuthContext);

const projectToLed = (type: string, data: any) => {
    axios.post('http://' + window.location.hostname + ':8000/led_state', { type, data })
         .then(() => alert("Đã chuyển tín hiệu lên màn LED"))
         .catch(() => alert("Lỗi kết nối màn LED"))
};
`;

lines.splice(2, 0, injection);
let text = lines.join('\n');

// DrawScreen useAuth inject
text = text.replace(/function DrawScreen[^{]+{[^{]+{.*?}[^{]+{/, (m) => {
    return m + '\n  const { isAdmin } = useAuth();';
});

fs.writeFileSync('src/App.tsx', text, 'utf8');
console.log('Fixed authcontext');
