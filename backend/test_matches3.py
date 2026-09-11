from database import SessionLocal
import models
import codecs

db = SessionLocal()
matches = db.query(models.Match).filter(models.Match.category_id == 2).all()
with codecs.open('matches.txt', 'w', 'utf-8') as f:
    for m in matches:
        f.write(f"Cat {m.category_id}: {m.match_code}\n")
