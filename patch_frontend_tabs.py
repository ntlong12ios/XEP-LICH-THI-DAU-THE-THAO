import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\frontend\src\App.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_states = """const [activeCatId, setActiveCatId] = useState<number | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('teams')"""

new_states = """const [activeCatId, setActiveCatId] = useState<number | null>(() => {
    const saved = localStorage.getItem('activeCatId')
    return saved ? parseInt(saved) : null
  })
  const [activeTab, setActiveTab] = useState<TabType>(() => {
    return (localStorage.getItem('activeTab') as TabType) || 'teams'
  })

  useEffect(() => {
    if (activeCatId !== null) localStorage.setItem('activeCatId', activeCatId.toString())
  }, [activeCatId])

  useEffect(() => {
    localStorage.setItem('activeTab', activeTab)
  }, [activeTab])"""

if old_states in content:
    content = content.replace(old_states, new_states)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched App.tsx activeTab persistence")
else:
    print("Could not find old_states block in App.tsx")
