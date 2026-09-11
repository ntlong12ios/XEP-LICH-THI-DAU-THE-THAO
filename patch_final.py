import codecs

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'r', 'utf-8') as f:
    text = f.read()

target_draw = "<span>{isFootball ? '⚽' : '🏓'} {code}</span>"
rep_draw = "<span>{isFootball ? '⚽' : '🏓'} {code}</span>\n                  {isAdmin && <button className='btn-sm btn-ghost' style={{color:'white', borderColor:'white', marginLeft: 10}} onClick={(e)=>{e.stopPropagation(); projectToLed('bracket', {matchNum, slotList, category, isFootball})}}>📺 Chiếu LED</button>}"
text = text.replace(target_draw, rep_draw)

target_sched = "<span>{isFootball ? '⚽' : '🏓'} Lịch thi đấu: {date}</span>"
rep_sched = "<span>{isFootball ? '⚽' : '🏓'} Lịch thi đấu: {date} {isAdmin && <button className='btn-sm btn-ghost' style={{color:'white', borderColor:'white', marginLeft: 10}} onClick={()=>{projectToLed('schedule', {date, matches: dayMatches, category})}}>📺 Chiếu LED</button>}</span>"
text = text.replace(target_sched, rep_sched)

with codecs.open(r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx', 'w', 'utf-8') as f:
    f.write(text)
print('Done!')
