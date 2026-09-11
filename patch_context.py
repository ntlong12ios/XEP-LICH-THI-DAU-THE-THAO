import re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add context and projectToLed at the top of the file
context_code = '''import { createContext, useContext } from 'react'

const AuthContext = createContext({ isAdmin: false })
export const useAuth = () => useContext(AuthContext)

const projectToLed = (type: string, data: any) => {
    axios.post(${API}/led_state, { type, data })
         .then(() => alert("Đã chuyển tín hiệu lên màn LED"))
         .catch(() => alert("Lỗi kết nối màn LED"))
}
'''
text = text.replace("const API = http://:8000", context_code + "\nconst API = http://:8000")

# 2. Modify App() to provide context and show login
app_login_state = '''  const [isAdmin, setIsAdmin] = useState(() => localStorage.getItem('isAdmin') === 'true')
  const [showLogin, setShowLogin] = useState(false)
  const [password, setPassword] = useState('')

  const handleLogin = () => {
    axios.post(${API}/verify_admin, { password }).then(res => {
      if(res.data.success) {
        localStorage.setItem('isAdmin', 'true'); setIsAdmin(true); setShowLogin(false);
      } else {
        alert("Sai mật khẩu");
      }
    })
  }

  const handleLogout = () => { localStorage.removeItem('isAdmin'); setIsAdmin(false); }
'''
text = text.replace("const [activeTab, setActiveTab] = useState<TabType>('teams')", "const [activeTab, setActiveTab] = useState<TabType>('teams')\n" + app_login_state)

# Wrap return of App() in Context Provider
text = text.replace('<div className="app-layout">', '<AuthContext.Provider value={{ isAdmin }}><div className="app-layout">')
text = text.replace('</main>\n    </div>\n  )\n}', '</main>\n    </div>\n    {showLogin && <div style={{position: "fixed", top:0, left:0, right:0, bottom:0, background: "rgba(0,0,0,0.5)", zIndex: 9999, display: "flex", alignItems: "center", justifyContent: "center"}}><div style={{background: "white", padding: 30, borderRadius: 12, textAlign: "center"}}><h2>Đăng nhập Admin</h2><input type="password" value={password} onChange={e=>setPassword(e.target.value)} style={{padding: 10, margin: "20px 0", width: "100%", fontSize: 18}}/><br/><button className="btn btn-primary" onClick={handleLogin}>Đăng nhập</button> <button className="btn btn-ghost" onClick={()=>setShowLogin(false)}>Hủy</button></div></div>}\n    </AuthContext.Provider>\n  )\n}')

# Add Login button to header
header_btn = '''<div className="header-spacer" />
          {!isAdmin ? <button className="btn btn-ghost" style={{color:"white", borderColor:"rgba(255,255,255,0.5)"}} onClick={()=>setShowLogin(true)}>🔒 Admin Login</button> : <button className="btn btn-ghost" style={{color:"white", borderColor:"rgba(255,255,255,0.5)"}} onClick={handleLogout}>🔓 Thoát Admin</button>}'''
text = text.replace('<div className="header-spacer" />', header_btn, 1)

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("App context patched!")
