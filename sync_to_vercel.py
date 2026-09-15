"""
sync_to_vercel.py
=================
Đồng bộ toàn bộ dữ liệu bốc thăm + lịch thi đấu từ local SQLite lên Vercel.

Chạy: python sync_to_vercel.py
"""
import sqlite3
import sys
import os
import time
import requests

sys.stdout.reconfigure(encoding='utf-8')

# ─── CẤU HÌNH ────────────────────────────────────────────────────────────────
VERCEL_URL = "https://xep-lich-thi-dau-the-thao-sandy.vercel.app/api"
LOCAL_DB   = os.path.join(os.path.dirname(__file__), "backend", "sport_tournament.db")
EXCEL_FILE = os.path.join(os.path.dirname(__file__), "DATA.xlsx")

# Cấu hình bracket theo category (đọc từ DB local)
# cat=1 Bóng đá nam:        knockout
# cat=2 Pickleball đôi nam: knockout
# cat=3 Pickleball đôi nam-nữ: round_robin, 8 bảng
# cat=4 Pickleball đôi nữ:  knockout
BRACKET_CONFIG = {
    1: {"format": "knockout"},
    2: {"format": "knockout"},
    3: {"format": "round_robin", "num_groups": 8},
    4: {"format": "knockout"},
}
# ─────────────────────────────────────────────────────────────────────────────

def ok(r):
    if r.status_code >= 400:
        print(f"    ❌ HTTP {r.status_code}: {r.text[:200]}")
        return False
    return True

def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print('='*60)

# ── BƯỚC 1: Upload Excel để tạo lại categories + teams ───────────────────────
step("BƯỚC 1: Upload Excel → tạo categories & teams")
with open(EXCEL_FILE, "rb") as f:
    r = requests.post(
        f"{VERCEL_URL}/upload_excel",
        files={"file": ("DATA.xlsx", f,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        timeout=60
    )
if not ok(r):
    print("❌ Upload Excel thất bại, dừng lại.")
    sys.exit(1)
print(f"  ✅ {r.json().get('message', 'OK')}")
time.sleep(2)  # Đợi DB ghi xong

# ── Lấy danh sách categories & teams từ Vercel ───────────────────────────────
vercel_categories = requests.get(f"{VERCEL_URL}/categories", timeout=30).json()
vercel_teams_all  = requests.get(f"{VERCEL_URL}/teams", timeout=30).json()

# Map draw_code → vercel team_id
draw_to_vercel_team = {t["draw_code"]: t["id"] for t in vercel_teams_all if t.get("draw_code")}
print(f"  Teams trên Vercel: {len(vercel_teams_all)} | map draw_code: {len(draw_to_vercel_team)}")

# ── BƯỚC 2: Đọc local DB ─────────────────────────────────────────────────────
step("BƯỚC 2: Đọc dữ liệu local DB")
con = sqlite3.connect(LOCAL_DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("SELECT * FROM bracket_slots ORDER BY category_id, match_number, position_in_match")
local_slots = cur.fetchall()

cur.execute("""SELECT m.*, t1.draw_code AS dc1, t2.draw_code AS dc2
               FROM matches m
               LEFT JOIN teams t1 ON t1.id = m.team1_id
               LEFT JOIN teams t2 ON t2.id = m.team2_id
               ORDER BY m.category_id, m.id""")
local_matches = cur.fetchall()

cur.execute("SELECT * FROM teams")
local_teams = {t["id"]: dict(t) for t in cur.fetchall()}
con.close()

# Map (category_id, match_number, position_in_match) → local team draw_code
slot_key_to_draw = {}
for s in local_slots:
    team = local_teams.get(s["team_id"])
    draw = team["draw_code"] if team else None
    slot_key_to_draw[(s["category_id"], s["match_number"], s["position_in_match"])] = draw

print(f"  Local slots: {len(local_slots)} | Assignments: {sum(1 for v in slot_key_to_draw.values() if v)}")
print(f"  Local matches: {len(local_matches)}")

# ── BƯỚC 3: Generate bracket + assign cho từng category ──────────────────────
step("BƯỚC 3: Generate bracket & gán đội vào slot")

for cat in vercel_categories:
    cat_id   = cat["id"]
    cat_name = cat["name"]
    cfg      = BRACKET_CONFIG.get(cat_id, {"format": "knockout"})

    print(f"\n  📋 [{cat_id}] {cat_name} — format={cfg['format']}")

    # 3a. Generate bracket trên Vercel
    payload = {"format": cfg["format"]}
    if "num_groups" in cfg:
        payload["num_groups"] = cfg["num_groups"]

    r = requests.post(f"{VERCEL_URL}/categories/{cat_id}/generate_bracket",
                      json=payload, timeout=30)
    if not ok(r):
        print(f"    ⚠️  Bỏ qua category {cat_id}")
        continue
    vercel_slots = r.json()
    print(f"    Tạo {len(vercel_slots)} slots trên Vercel")
    time.sleep(0.5)

    # 3b. Build map (match_number, position_in_match) → vercel slot_id
    vslot_key_to_id = {
        (vs["match_number"], vs["position_in_match"]): vs["id"]
        for vs in vercel_slots
    }

    # 3c. Gán đội
    assigned = 0
    failed   = 0
    for (c_id, match_num, pos), draw_code in slot_key_to_draw.items():
        if c_id != cat_id or not draw_code:
            continue
        vercel_slot_id = vslot_key_to_id.get((match_num, pos))
        vercel_team_id = draw_to_vercel_team.get(draw_code)
        if not vercel_slot_id or not vercel_team_id:
            failed += 1
            continue
        r = requests.put(
            f"{VERCEL_URL}/bracket_slots/{vercel_slot_id}/assign",
            json={"team_id": vercel_team_id},
            timeout=15
        )
        if ok(r):
            assigned += 1
        else:
            failed += 1
        time.sleep(0.05)  # Tránh rate limit

    print(f"    ✅ Assigned {assigned} slots | ❌ Failed {failed}")

# ── BƯỚC 4: Generate matches từ bracket slots ─────────────────────────────────
step("BƯỚC 4: Generate matches từ bracket")

for cat in vercel_categories:
    cat_id   = cat["id"]
    cat_name = cat["name"]
    print(f"\n  🏆 [{cat_id}] {cat_name}")
    r = requests.post(f"{VERCEL_URL}/categories/{cat_id}/generate_matches", timeout=60)
    if ok(r):
        data = r.json()
        print(f"    ✅ Tạo {data.get('matches_created', '?')} trận")
    time.sleep(1)

# ── BƯỚC 5: Đồng bộ lịch thi đấu ────────────────────────────────────────────
step("BƯỚC 5: Đồng bộ lịch thi đấu")

# Lấy matches trên Vercel (sau khi generate)
vercel_matches_raw = requests.get(f"{VERCEL_URL}/matches", timeout=30).json()

# Map (category_id, match_code) → vercel match_id
vcode_to_id = {}
for vm in vercel_matches_raw:
    key = (vm["category_id"], vm["match_code"])
    vcode_to_id[key] = vm["id"]

print(f"  Vercel matches: {len(vercel_matches_raw)}")

sched_ok = 0
sched_fail = 0
for lm in local_matches:
    if not lm["scheduled_time"] and not lm["court"]:
        continue
    key = (lm["category_id"], lm["match_code"])
    vercel_match_id = vcode_to_id.get(key)
    if not vercel_match_id:
        # Thử đảo match_code (vd: "A-B" vs "B-A")
        code = lm["match_code"] or ""
        if "-" in code:
            parts = [p.strip() for p in code.split("-", 1)]
            reversed_code = f"{parts[1]}-{parts[0]}"
            key2 = (lm["category_id"], reversed_code)
            vercel_match_id = vcode_to_id.get(key2)
    if not vercel_match_id:
        sched_fail += 1
        continue

    r = requests.put(
        f"{VERCEL_URL}/matches/{vercel_match_id}/schedule",
        json={
            "scheduled_time": lm["scheduled_time"],
            "court": lm["court"]
        },
        timeout=15
    )
    if ok(r):
        sched_ok += 1
    else:
        sched_fail += 1
    time.sleep(0.05)

print(f"  ✅ Lịch đồng bộ: {sched_ok} trận | ❌ Không tìm thấy: {sched_fail}")

# ── HOÀN TẤT ─────────────────────────────────────────────────────────────────
step("✅ HOÀN TẤT — Kiểm tra nhanh trên Vercel")
r = requests.get(f"{VERCEL_URL}/categories", timeout=15)
cats = r.json()
for c in cats:
    teams_r = requests.get(f"{VERCEL_URL}/categories/{c['id']}/teams", timeout=15)
    teams = teams_r.json()
    matches_r = requests.get(f"{VERCEL_URL}/categories/{c['id']}/matches", timeout=15)
    matches = matches_r.json()
    sched = sum(1 for m in matches if m.get("scheduled_time"))
    print(f"  [{c['id']}] {c['name']}: {len(teams)} đội | {len(matches)} trận ({sched} có lịch)")

print("\n🎉 Xong! Truy cập https://xep-lich-thi-dau-the-thao-sandy.vercel.app/")
