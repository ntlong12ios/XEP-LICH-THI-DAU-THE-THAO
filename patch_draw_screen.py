import os
import re

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# First, insert orderedSlots and getGlobalSlotNum calculation before the return inside DrawScreen
# We can find `const filteredEntries = Object.entries(matchGroups)` if it exists.
# Let's find where to put the helper. 
# `const assignedCount = assignedIds.size` is at line 210.
injection_point = "const assignedCount = assignedIds.size"
helper_code = """const assignedCount = assignedIds.size

  const orderedSlots = slots.slice().sort((a, b) => {
    if (a.match_number !== b.match_number) return a.match_number - b.match_number;
    return a.position_in_match - b.position_in_match;
  });
  const getGlobalSlotNum = (slotId: number) => {
    const idx = orderedSlots.findIndex(s => s.id === slotId);
    return idx >= 0 ? idx + 1 : 0;
  };"""
content = content.replace(injection_point, helper_code)


# Next, replace the <div className="slot-position">Đội {pos + 1}</div>
old_slot = '<div className="slot-position">Đội {pos + 1}</div>'
new_slot = """<div className="slot-position" style={{display: 'flex', flexDirection: 'column'}}>
                        <span>Đội {pos + 1}</span>
                        <span style={{color: '#d32f2f', fontWeight: 'bold', fontSize: '1.1rem', marginTop: 12, marginBottom: 12}}>
                          Số {getGlobalSlotNum(slot.id).toString().padStart(2, '0')}
                        </span>
                      </div>"""
content = content.replace(old_slot, new_slot)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched DrawScreen")
