import sqlite3

# Path to the SQLite database
db_path = "db.sqlite3"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Retrieve the schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
schema = cursor.fetchall()
conn.close()

# Print the schema
for table in schema:
    if table[0]:
        print(table[0])
