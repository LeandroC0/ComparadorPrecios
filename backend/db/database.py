import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Base

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no definido")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_tablas():
    Base.metadata.create_all(bind=engine)
