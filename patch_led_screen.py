import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add getGlobalSlotNum helper right after fetching slots or inside the component before it renders
# Wait, let's just insert it at the very top of `export default function LedScreen() {`?
# No, it needs `slots`. Let's just insert it before `if (ledState.type === 'all_brackets') {`
helper_code = """  const orderedSlots = slots.slice().sort((a: any, b: any) => {
    if (a.match_number !== b.match_number) return a.match_number - b.match_number;
    return a.position_in_match - b.position_in_match;
  });
  const getGlobalSlotNum = (slotId: number) => {
    const idx = orderedSlots.findIndex((s: any) => s.id === slotId);
    return idx >= 0 ? idx + 1 : 0;
  };
"""
content = content.replace("if (ledState.type === 'all_brackets') {", helper_code + "\n  if (ledState.type === 'all_brackets') {")

# For 'all_brackets'
old_slot_1 = '<div className="slot-position">Đội {idx + 1}</div>'
new_slot_1 = """<div className="slot-position" style={{display: 'flex', flexDirection: 'column'}}>
                        <span>Đội {idx + 1}</span>
                        <span style={{color: '#d32f2f', fontWeight: 'bold', fontSize: '1.1rem', marginTop: 12, marginBottom: 12}}>
                          Số {getGlobalSlotNum(slot.id).toString().padStart(2, '0')}
                        </span>
                      </div>"""
content = content.replace(old_slot_1, new_slot_1)

# For 'bracket' (Wait, it's identical text!)
# Wait, the replace function with default count replaces ALL occurrences.
# Let's verify there are exactly two occurrences of `<div className="slot-position">Đội {idx + 1}</div>`.
# Yes, one in `all_brackets` loop, one in `bracket` loop.
# `replace` string replaces ALL occurrences!

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched LedScreen")
