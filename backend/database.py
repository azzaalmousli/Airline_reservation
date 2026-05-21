# database.py
import mysql.connector
from contextlib import contextmanager
from config import settings


def get_db_connection():
    """Returns a fresh MySQL connection using settings loaded from .env."""
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        port=settings.DB_PORT
    )


@contextmanager
def db_cursor():
    """
    Context manager that yields (conn, cursor) with a dictionary cursor.
    Commits on clean exit, rolls back and re-raises on any exception,
    and always closes both cursor and connection.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
