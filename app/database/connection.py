from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# 1. Define your engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Define SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
