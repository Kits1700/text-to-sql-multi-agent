"""
sql_executor.py — runs a SQL query against a SQLite database.

Returns the results if it works, or the error message if it fails.
That error gets passed back to the generator to fix on the next attempt.
"""

import sqlite3


def run_sql(sql_query: str, db_path: str) -> dict:
    try:
        conn   = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        rows    = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()

        return {
            "success": True,
            "columns": columns,
            "data":    rows,
            "error":   None,
        }

    except Exception as e:
        return {
            "success": False,
            "columns": [],
            "data":    None,
            "error":   str(e),
        }
