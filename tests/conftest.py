import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import TEST_DATABASE_URL_FILE_BASED, TEST_IN_MEMORY_DB
from app.database.base import Base
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from sqlalchemy.pool import StaticPool

# In-memory DB plus static pool
engine = create_engine(
    TEST_IN_MEMORY_DB,  # in-memory db
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # required for shared connection
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# autouse fixure for setup/tear down
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ovveride DB dependecny
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    # Override dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Create client AFTER override
    with TestClient(app) as c:
        yield c

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
