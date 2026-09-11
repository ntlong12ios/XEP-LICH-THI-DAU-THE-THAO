from database import SessionLocal
import models
import codecs

db = SessionLocal()
matches = db.query(models.Match).all()
with codecs.open('matches.txt', 'w', 'utf-8') as f:
    for m in matches:
        if m.category_id > 1 and ('3' in m.match_code or '4' in m.match_code or 'Ba' in m.match_code):
            f.write(f"Cat {m.category_id}: {m.match_code}\n")
