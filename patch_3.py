with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add button to DrawScreen header
target_draw = "<span>{isFootball ? '⚽' : '🏓'} {code}</span>"
rep_draw = "<span>{isFootball ? '⚽' : '🏓'} {code}</span>\n                  {isAdmin && <button className=\\"btn-sm btn-ghost\\" style={{color:\\"white\\", borderColor:\\"white\\", marginLeft: 10}} onClick={(e)=>{e.stopPropagation(); projectToLed('bracket', {matchNum, slotList, category, isFootball})}}>📺 Chiếu LED</button>}"
text = text.replace(target_draw, rep_draw)

# Add button to ScheduleScreen header
target_sched = "<span>{isFootball ? '⚽' : '🏓'} Lịch thi đấu: {date}</span>"
rep_sched = "<span>{isFootball ? '⚽' : '🏓'} Lịch thi đấu: {date} {isAdmin && <button className=\\"btn-sm btn-ghost\\" style={{color:\\"white\\", borderColor:\\"white\\", marginLeft: 10}} onClick={()=>{projectToLed('schedule', {date, matches: dayMatches, category})}}>📺 Chiếu LED</button>}</span>"
text = text.replace(target_sched, rep_sched)

with open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch 3!")
