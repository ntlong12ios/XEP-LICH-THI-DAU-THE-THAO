import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\LedScreen.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

broken_str = """                        </div>
                      )}
        return { ...s, team: teams.find((t:any) => t.id === s.team_id) || s.team }"""

fixed_str = """                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )
          })}
        </div>
      </div>
    </div>
    )
  }

  if (ledState.type === 'bracket') {
    const { matchNum, isFootball, slotList } = ledState.data
    const currentSlots = slots.length > 0 ? slots : slotList;
    if (!currentSlots) return <div style={{padding: 40}}>Loading match...</div>

    const latestSlots = currentSlots.map((s:any) => {
        return { ...s, team: teams.find((t:any) => t.id === s.team_id) || s.team }"""

content = content.replace(broken_str, fixed_str)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed damage")
