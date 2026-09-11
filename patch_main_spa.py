import os
import sys

content = ""
with open("backend/main.py", "r", encoding="utf-8") as f:
    content = f.read()

static_code = """
import os
import sys
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

frontend_dist = os.path.join(base_dir, "frontend_dist")

# Mount assets directory
if os.path.exists(os.path.join(frontend_dist, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    path = os.path.join(frontend_dist, full_path)
    if full_path and os.path.isfile(path):
        return FileResponse(path)
    return FileResponse(os.path.join(frontend_dist, "index.html"))
"""

if "serve_spa" not in content:
    with open("backend/main.py", "a", encoding="utf-8") as f:
        f.write("\n" + static_code)
    print("Patched main.py with SPA serving code")
else:
    print("Already patched")
