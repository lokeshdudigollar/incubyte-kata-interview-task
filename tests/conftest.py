import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base

# Use an in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Teardown: Drop everything after the test
    session.close()
    Base.metadata.drop_all(bind=engine)