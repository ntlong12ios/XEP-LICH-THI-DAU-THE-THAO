import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """
from fastapi import File, UploadFile
import io

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        import_excel.run_import(file_obj=io.BytesIO(contents))
        return {"message": "Cập nhật dữ liệu từ file Excel thành công!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

if 'upload_excel' not in content:
    content = content.replace('import import_excel', 'import import_excel' + new_route)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added /upload_excel route')
else:
    print('Route already exists')
