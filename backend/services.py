# services.py
from decimal import Decimal
from datetime import datetime, date

from database import get_db_connection


def log_performance(operation_name: str, execution_time_ms: float, status: str = 'Success'):
    """
    Inserts a record into system_performance_log.
    Silently swallows all errors so logging never breaks an API request.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO system_performance_log
               (operation_name, execution_time_ms, status)
               VALUES (%s, %s, %s)""",
            (operation_name[:100], round(execution_time_ms, 2), status[:20])
        )
        conn.commit()
    except Exception:
        pass
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


def serialize_row(row: dict) -> dict:
    """
    Converts Decimal and datetime types in a DB result row to JSON-safe Python types.
    MySQL Connector returns these native types that Flask's jsonify cannot handle.
    """
    result = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, (datetime, date)):
            result[key] = str(value)
        else:
            result[key] = value
    return result
