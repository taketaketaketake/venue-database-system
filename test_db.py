# test_db.py
from src.utils.db_utils import connect_db, execute_query
conn = connect_db()
results = execute_query(conn, "SELECT name, address, category FROM venues")
for row in results:
    print(f"{row['name']}, {row['address']}, {row['category']}")
