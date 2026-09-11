from database import SessionLocal
import models
from sqlalchemy import func

db = SessionLocal()
res = db.query(models.Match.category_id, func.count(models.Match.id)).group_by(models.Match.category_id).all()
print(res)
