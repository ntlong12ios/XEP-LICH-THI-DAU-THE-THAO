import codecs
import re

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Fix literal \n
text = text.replace('\\n', '\n')

# Fix backticks
text = text.replace('axios.post(${API}/verify_admin', 'axios.post(`${API}/verify_admin`')

# Fix closing braces for buttons
text = text.replace('}}>📊 Xuất Excel</button>', '}}>📊 Xuất Excel</button>}')
text = text.replace('}}>📊 Xuất Excel</button>}}', '}}>📊 Xuất Excel</button>}')

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Fixed!")
