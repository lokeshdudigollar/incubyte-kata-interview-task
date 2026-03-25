from app.database import engine


def test_database_connection():
    connection = engine.connect()
    assert connection is not None
    connection.close()
