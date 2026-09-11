import re

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Schedule DragDrop
text = text.replace('<DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>', '{isAdmin ? <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}> : <div className="schedule-timeline">}')
text = text.replace('</DndContext>', '{isAdmin ? </DndContext> : </div>}')

# ResultsScreen Admin
text = text.replace('function ResultsScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {', 'function ResultsScreen({ category, onRefresh }: { category: Category; onRefresh: () => void }) {\\n  const { isAdmin } = useAuth();')
text = text.replace('<input\\n\\n                            className="score-input"', '{!isAdmin ? <span>{m.score1 !== null ? m.score1 : "-"}</span> : <input\\n\\n                            className="score-input"')
text = text.replace('placeholder="-"\\n\\n                          />', 'placeholder="-"\\n\\n                          />}')

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch 2!")
