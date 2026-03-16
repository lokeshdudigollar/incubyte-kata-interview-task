import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")