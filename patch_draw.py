import codecs

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', 'utf-8') as f:
    text = f.read()

draw_start = text.find('function DrawScreen')
sched_start = text.find('function ScheduleScreen')
draw_chunk = text[draw_start:sched_start]

target = '📄 Xuất PDF</button>}'
replace = target + '\n        {isAdmin && <button className="btn btn-secondary" style={{backgroundColor: \'#1565C0\', color: \'white\', borderColor: \'#1565C0\'}} onClick={() => projectToLed(\'all_brackets\', { categoryId: category.id, drawFormat, isFootball: category.name.toLowerCase().includes(\'bóng đá\') })}>📺 Chiếu toàn bộ LED</button>}'

new_draw = draw_chunk.replace(target, replace, 1)
text = text[:draw_start] + new_draw + text[sched_start:]

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', 'utf-8') as f:
    f.write(text)
print("Button added to App.tsx")
