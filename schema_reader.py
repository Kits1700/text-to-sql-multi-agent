"""
schema_reader.py
----------------
Dynamically reads the structure of a SQLite database.
Returns a text description of all tables and columns.

This is used by the Generator Agent so it knows
exactly what tables and columns exist - without
anything being hardcoded.
"""

import sqlite3


def get_schema(db_path: str) -> str:
    """
    Reads the database structure dynamically.

    Args:
        db_path: path to the .sqlite file

    Returns:
        A text string describing all tables and columns.
        Example:
            Table: stadium
              - Stadium_ID (int)
              - Location (text)
              - Name (text)
    """

    # Connect to the SQLite database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ask SQLite for all table names in this database
    # sqlite_master is a built-in table that stores the database structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()  # e.g. [('stadium',), ('singer',)]

    schema_text = ""

    # Loop through each table and get its column details
    for (table_name,) in tables:
        schema_text += f"Table: {table_name}\n"

        # PRAGMA table_info returns metadata about each column
        # Each row: (index, name, type, notnull, default_value, is_primary_key)
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()

        for col in columns:
            col_name = col[1]   # column name e.g. "Stadium_ID"
            col_type = col[2]   # column type e.g. "int", "text", "real"
            schema_text += f"  - {col_name} ({col_type})\n"

        schema_text += "\n"

    conn.close()
    return schema_text
