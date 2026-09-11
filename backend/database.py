import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read DATABASE_URL from environment, fallback to sqlite
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Use /tmp for sqlite on Vercel to avoid read-only filesystem errors
    if os.environ.get("VERCEL"):
        DB_PATH = "/tmp/sport_tournament.db"
    else:
        DB_PATH = os.path.join(BASE_DIR, "sport_tournament.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
else:
    # If postgresql URL starts with postgres://, replace with postgresql:// for SQLAlchemy
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL

# SQLite needs check_same_thread=False
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
