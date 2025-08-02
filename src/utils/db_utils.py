import sqlite3
from pathlib import Path

def connect_db(db_path='data/venues.db'):
    try:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_query(conn, query, params=()):
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return results
        conn.commit()
        return None
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        raise

def close_db(conn):
    try:
        conn.close()
    except sqlite3.Error as e:
        print(f"Error closing database: {e}")
        raise
