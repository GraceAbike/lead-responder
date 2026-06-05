from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = BASE_DIR.parent / "leads.db"
raw_database_url = os.getenv("DATABASE_URL", "").strip()

# Render may receive an invalid Windows-style SQLite path from local .env uploads.
if raw_database_url.startswith("sqlite:///C:/") or raw_database_url.startswith("sqlite:///C:\\"):
    raw_database_url = ""

DATABASE_URL = raw_database_url or f"sqlite:///{DEFAULT_DB.as_posix()}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
