import os
import sys
import re

with open("backend/database.py", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"BASE_DIR = os\.path\.dirname\(os\.path\.abspath\(__file__\)\)",
    """import sys
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))""",
    content
)

with open("backend/database.py", "w", encoding="utf-8") as f:
    f.write(new_content)
    
print("Patched database.py for PyInstaller compatibility")
