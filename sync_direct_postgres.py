"""
sync_direct_postgres.py
========================
Kết nối THẲNG vào Supabase PostgreSQL (bỏ qua Vercel API).
Copy toàn bộ dữ liệu từ local SQLite → Supabase.

Chạy: python sync_direct_postgres.py
Hoặc: python sync_direct_postgres.py "postgresql://..."  (truyền URL qua argument)
"""
import sqlite3
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# ─── CONNECTION STRING ────────────────────────────────────────────────────────
# Lấy từ Vercel Environment Variables (DATABASE_URL)
# Có thể truyền qua argument: python sync_direct_postgres.py "postgresql://..."
if len(sys.argv) > 1:
    PG_URL = sys.argv[1]
else:
    PG_URL = input(
        "\n📌 Dán connection string Supabase (từ Vercel > Settings > DATABASE_URL):\n> "
    ).strip()

if not PG_URL.startswith("postgresql"):
    print("❌ URL không hợp lệ. Phải bắt đầu bằng postgresql://")
    sys.exit(1)

LOCAL_DB = os.path.join(os.path.dirname(__file__), "backend", "sport_tournament.db")

# ─── KẾT NỐI POSTGRESQL ──────────────────────────────────────────────────────
print(f"\n🔌 Kết nối Supabase...")
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Với Supabase pooler (port 6543) cần thêm tham số
pg_url = PG_URL
if "sslmode" not in pg_url:
    pg_url += ("&" if "?" in pg_url else "?") + "sslmode=require"

# SQLAlchemy cần prefix psycopg2
if pg_url.startswith("postgresql://"):
    sa_url = pg_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    sa_url = pg_url

try:
    engine = create_engine(sa_url, connect_args={"connect_timeout": 15})
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
    print("  ✅ Kết nối thành công!")
except Exception as e:
    print(f"  ❌ Lỗi kết nối: {e}")
    sys.exit(1)

# ─── TẠO BẢNG (dùng models của app) ─────────────────────────────────────────
print("\n🏗️  Tạo bảng trên PostgreSQL...")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
os.environ["DATABASE_URL"] = pg_url  # Dùng PG thay SQLite

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id   = Column(Integer, primary_key=True)
    name = Column(String)
    sport= Column(String)

class Team(Base):
    __tablename__ = "teams"
    id            = Column(Integer, primary_key=True)
    name          = Column(String)
    contact_name  = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    category_id   = Column(Integer, ForeignKey("categories.id"))
    draw_code     = Column(String, nullable=True)

class Athlete(Base):
    __tablename__ = "athletes"
    id      = Column(Integer, primary_key=True)
    name    = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))

class BracketSlot(Base):
    __tablename__ = "bracket_slots"
    id                = Column(Integer, primary_key=True)
    category_id       = Column(Integer, ForeignKey("categories.id"))
    slot_code         = Column(String)
    round_number      = Column(Integer)
    match_number      = Column(Integer)
    slot_index        = Column(Integer)
    position_in_match = Column(Integer)
    label             = Column(String, nullable=True)
    team_id           = Column(Integer, ForeignKey("teams.id"), nullable=True)

class Match(Base):
    __tablename__ = "matches"
    id                  = Column(Integer, primary_key=True)
    match_code          = Column(String)
    category_id         = Column(Integer, ForeignKey("categories.id"))
    team1_id            = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team2_id            = Column(Integer, ForeignKey("teams.id"), nullable=True)
    score1              = Column(Integer, nullable=True)
    score2              = Column(Integer, nullable=True)
    status              = Column(String, default="pending")
    next_match_id       = Column(Integer, ForeignKey("matches.id"), nullable=True)
    loser_next_match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    scheduled_time      = Column(String, nullable=True)
    court               = Column(String, nullable=True)

class AppState(Base):
    __tablename__ = "app_state"
    key   = Column(String, primary_key=True)
    value = Column(String)

Base.metadata.create_all(bind=engine)
print("  ✅ Bảng đã sẵn sàng")

# ─── ĐỌC DỮ LIỆU TỪ SQLITE ──────────────────────────────────────────────────
print("\n📖 Đọc dữ liệu local SQLite...")
con = sqlite3.connect(LOCAL_DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

cats     = [dict(r) for r in cur.execute("SELECT * FROM categories ORDER BY id")]
teams    = [dict(r) for r in cur.execute("SELECT * FROM teams ORDER BY id")]
athletes = [dict(r) for r in cur.execute("SELECT * FROM athletes ORDER BY id")]
slots    = [dict(r) for r in cur.execute("SELECT * FROM bracket_slots ORDER BY id")]
matches  = [dict(r) for r in cur.execute("SELECT * FROM matches ORDER BY id")]
con.close()

print(f"  categories={len(cats)}, teams={len(teams)}, athletes={len(athletes)}")
print(f"  bracket_slots={len(slots)}, matches={len(matches)}")

# ─── XÓA DỮ LIỆU CŨ TRÊN POSTGRES (theo thứ tự FK) ─────────────────────────
print("\n🗑️  Xóa dữ liệu cũ trên Supabase...")
Session = sessionmaker(bind=engine)
db = Session()
try:
    db.execute(text("DELETE FROM matches"))
    db.execute(text("DELETE FROM bracket_slots"))
    db.execute(text("DELETE FROM athletes"))
    db.execute(text("DELETE FROM teams"))
    db.execute(text("DELETE FROM categories"))
    db.commit()
    print("  ✅ Đã xóa dữ liệu cũ")
except Exception as e:
    db.rollback()
    print(f"  ⚠️  {e}")

# ─── RESET SEQUENCES (PostgreSQL auto-increment) ─────────────────────────────
for tbl in ["categories", "teams", "athletes", "bracket_slots", "matches"]:
    try:
        db.execute(text(f"ALTER SEQUENCE {tbl}_id_seq RESTART WITH 1"))
    except:
        db.rollback()

# ─── INSERT DỮ LIỆU ──────────────────────────────────────────────────────────
def insert_batch(model, rows, label):
    if not rows:
        return
    try:
        db.bulk_insert_mappings(model, rows)
        db.commit()
        print(f"  ✅ {label}: {len(rows)} bản ghi")
    except Exception as e:
        db.rollback()
        print(f"  ❌ {label}: {e}")

print("\n📤 Insert dữ liệu vào Supabase...")
insert_batch(Category,    cats,     "categories")
insert_batch(Team,        teams,    "teams")
insert_batch(Athlete,     athletes, "athletes")
insert_batch(BracketSlot, slots,    "bracket_slots")

# Matches cần insert 2 lần vì next_match_id self-reference
# Lần 1: insert không có next_match_id
matches_no_ref = [{**m, "next_match_id": None, "loser_next_match_id": None} for m in matches]
insert_batch(Match, matches_no_ref, "matches (round 1)")

# Lần 2: update next_match_id
updated = 0
for m in matches:
    if m.get("next_match_id") or m.get("loser_next_match_id"):
        try:
            db.execute(
                text("UPDATE matches SET next_match_id=:nid, loser_next_match_id=:lid WHERE id=:id"),
                {"nid": m["next_match_id"], "lid": m["loser_next_match_id"], "id": m["id"]}
            )
            updated += 1
        except Exception as e:
            db.rollback()
            print(f"    ⚠️  match {m['id']}: {e}")
db.commit()
print(f"  ✅ matches next_match_id: cập nhật {updated} bản ghi")

# ─── RESET SEQUENCES đúng giá trị ────────────────────────────────────────────
print("\n🔧 Reset sequences...")
for tbl, rows in [("categories", cats), ("teams", teams), ("athletes", athletes),
                   ("bracket_slots", slots), ("matches", matches)]:
    if rows:
        max_id = max(r["id"] for r in rows)
        try:
            db.execute(text(f"SELECT setval('{tbl}_id_seq', {max_id})"))
        except:
            db.rollback()
db.commit()
print("  ✅ Sequences OK")

db.close()

# ─── KIỂM TRA KẾT QUẢ ────────────────────────────────────────────────────────
print("\n✅ KIỂM TRA KẾT QUẢ TRÊN SUPABASE:")
with engine.connect() as c:
    for tbl in ["categories", "teams", "athletes", "bracket_slots", "matches"]:
        cnt = c.execute(text(f"SELECT COUNT(*) FROM {tbl}")).fetchone()[0]
        print(f"  {tbl}: {cnt}")
    sched = c.execute(text("SELECT COUNT(*) FROM matches WHERE scheduled_time IS NOT NULL")).fetchone()[0]
    print(f"  matches có lịch: {sched}")

print("\n🎉 Sync hoàn tất! Truy cập: https://xep-lich-thi-dau-the-thao-sandy.vercel.app/")
