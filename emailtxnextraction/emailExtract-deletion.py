import csv
import re
import sqlite3
from datetime import datetime

# Delete records from both tables where the Date matches "DD-MM-YYYY HH:MM" format
def delete_records_by_date_format(cursor):
    # Date pattern matching the "DD-MM-YYYY HH:MM" format
    delete_query = """
        DELETE FROM home_addmoney_info WHERE Date LIKE '__-__-____ __:__'
    """
    cursor.execute(delete_query)

    delete_query1 = """
        DELETE FROM home_addmoney_info1 WHERE Date LIKE '__-__-____ __:__'
    """
    cursor.execute(delete_query1)

# Function to process the deletion based on the date format
def process_deletion_by_date_format(db_name):
    # Establishing database connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Delete records based on the provided date format
    delete_records_by_date_format(cursor)

    # Commit the changes
    conn.commit()

    # Optionally, fetch and print remaining rows from the tables
    cursor.execute("SELECT * FROM home_addmoney_info")
    print("\nRemaining records in home_addmoney_info:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM home_addmoney_info1")
    print("\nRemaining records in home_addmoney_info1:")
    for row in cursor.fetchall():
        print(row)

    # Close the database connection
    conn.close()

# Example usage
process_deletion_by_date_format(r"C:\Users\Lenova\OneDrive\Desktop\Source code\Source code\db.sqlite3")
