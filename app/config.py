import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
TEST_DATABASE_URL_FILE_BASED = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
TEST_IN_MEMORY_DB = os.getenv("TEST_IN_MEMORY_DB", "sqlite://")
