from database import SessionLocal
import models
import codecs

db = SessionLocal()
categories = db.query(models.Category).all()
with codecs.open('categories.txt', 'w', 'utf-8') as f:
    for c in categories:
        f.write(f"{c.id}: {c.name}\n")
