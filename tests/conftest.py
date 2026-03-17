import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import TEST_DATABASE_URL_FILE_BASED
from app.database.base import Base
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL_FILE_BASED, connect_args={"check_same_thread": False})
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Teardown: Drop everything after the test
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    engine = create_engine(TEST_DATABASE_URL_FILE_BASED, connect_args={"check_same_thread": False})

    TestingSessionLocal = sessionmaker(
        bind=engine
    )

    # create tables BEFORE override
    Base.metadata.create_all(bind=engine)

    # Override dependency 
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create client AFTER override
    with TestClient(app) as c:
        yield c

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()