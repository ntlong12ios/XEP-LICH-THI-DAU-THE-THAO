import re
path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """@app.post("/load_agenda")
async def load_agenda(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    import io
    try:
        contents = await file.read()
        wb = openpyxl.load_workbook(filename=io.BytesIO(contents), data_only=True)
        sheet = wb['Agenda']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file Excel: {str(e)}")"""

pattern = r'@app\.post\("/load_agenda"\)\s+def load_agenda\(db: Session = Depends\(database\.get_db\)\):\s+import os\s+base_dir = [^\n]+\s+file_path = [^\n]+\s+try:\s+wb = openpyxl\.load_workbook\(file_path, data_only=True\)\s+sheet = wb\[\'Agenda\'\]\s+except Exception as e:\s+raise HTTPException\(status_code=500, detail=[^\n]+\)'

if re.search(pattern, content):
    content = re.sub(pattern, new_route, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched backend load_agenda")
else:
    print("Pattern not found. Printing some context:")
    idx = content.find('load_agenda')
    print(content[idx:idx+500])
