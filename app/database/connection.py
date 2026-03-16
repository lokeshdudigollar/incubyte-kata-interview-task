from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Define your engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Define SessionLocal (THIS is what was missing)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)