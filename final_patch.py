import codecs
import re

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Make sure AuthContext exists
if "AuthContext" not in text:
    context_code = """import { createContext, useContext } from 'react'

const AuthContext = createContext({ isAdmin: false })
export const useAuth = () => useContext(AuthContext)

const projectToLed = (type: string, data: any) => {
    axios.post(`http://${window.location.hostname}:8000/led_state`, { type, data })
         .then(() => alert("Đã chuyển tín hiệu lên màn LED"))
         .catch(() => alert("Lỗi kết nối màn LED"))
}
"""
    text = text.replace("const API = `http://${window.location.hostname}:8000`", context_code + "\nconst API = `http://${window.location.hostname}:8000`")

# Ensure DrawScreen has isAdmin
if "const { isAdmin } = useAuth()" not in text.split("function DrawScreen")[1].split("return")[0]:
    text = text.replace('function DrawScreen({ category, teams, onRefresh }: {\n  category: Category; teams: Team[]; onRefresh: () => void\n}) {', 'function DrawScreen({ category, teams, onRefresh }: {\n  category: Category; teams: Team[]; onRefresh: () => void\n}) {\n  const { isAdmin } = useAuth();')

# Double isAdmin declarations
text = re.sub(r'const { isAdmin } = useAuth\(\);\s*const { isAdmin } = useAuth\(\);', 'const { isAdmin } = useAuth();', text)

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', 'utf-8') as f:
    f.write(text)

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'r', 'utf-8') as f:
    text2 = f.read()

text2 = text2.replace("`Trận ${matchNum}`", "`Trận ${matchNum}`").replace("Trận ${matchNum}", "`Trận ${matchNum}`")
text2 = text2.replace("`Bảng ${matchNum}`", "`Bảng ${matchNum}`").replace("Bảng ${matchNum}", "`Bảng ${matchNum}`")

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx', 'w', 'utf-8') as f:
    f.write(text2)

print("Final patch complete!")
