import re
import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_led_state = '''led_state = {"type": "none", "data": None}

@app.get("/led_state")
def get_led_state():
    return led_state

@app.post("/led_state")
def update_led_state(state: dict):
    global led_state
    led_state = state
    return {"success": True}'''

new_led_state = '''import json

@app.get("/led_state")
def get_led_state(db: Session = Depends(database.get_db)):
    state = db.query(models.AppState).filter(models.AppState.key == "led_state").first()
    if state and state.value:
        try:
            return json.loads(state.value)
        except:
            pass
    return {"type": "none", "data": None}

@app.post("/led_state")
def update_led_state(state: dict, db: Session = Depends(database.get_db)):
    state_str = json.dumps(state)
    db_state = db.query(models.AppState).filter(models.AppState.key == "led_state").first()
    if db_state:
        db_state.value = state_str
    else:
        db_state = models.AppState(key="led_state", value=state_str)
        db.add(db_state)
    db.commit()
    return {"success": True}'''

if old_led_state in content:
    content = content.replace(old_led_state, new_led_state)
else:
    # Use regex
    content = re.sub(r'led_state = \{"type".*?return \{"success": True\}', new_led_state, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
