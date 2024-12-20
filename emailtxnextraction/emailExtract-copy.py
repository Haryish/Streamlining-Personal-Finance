import csv
import re
import sqlite3
from datetime import datetime

# Categories mapping from categories.csv
def load_categories_mapping():
    categories_mapping = {}
    with open(r"C:\Users\Lenova\OneDrive\Desktop\Source code\Source code\emailtxnextraction\categories.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            keyword, category = row
            categories_mapping[keyword.lower()] = category.lower()  # Mapping keyword to category
    return categories_mapping

# Function to determine the category of the transaction
def determine_category(subject, body, categories_mapping):
    # Check if body contains relevant keywords for credit or debit transactions
    credit_keywords = ['refund', 'credit', 'received']
    debit_keywords = ['purchase', 'paid', 'expense', 'spent', 'transfer','withdrawn']

    # Amount extraction pattern
    amount_pattern = r'(\$|Rs\.?)\s?(\d+[\.,]?\d*)'

    category = None
    amount = None
    transaction_type = None

    # Check for keywords in subject or body and extract amount if available
    for keyword in credit_keywords:
        if keyword in body.lower():
            transaction_type = 'Income'  # Mark it as Income type
            amount_match = re.search(amount_pattern, body)
            if amount_match:
                amount = amount_match.group(2).replace(',', '')  # Remove commas for consistency
            break

    for keyword in debit_keywords:
        if keyword in body.lower():
            transaction_type = 'Income'  # Mark it as Income type
            amount_match = re.search(amount_pattern, body)
            if amount_match:
                amount = amount_match.group(2).replace(',', '')  # Remove commas for consistency
            break

    # Now, map the relevant keywords from the body to the categories
    if category is None:
        # If the category is not found, try to determine based on the CSV mapping
        for keyword, category_value in categories_mapping.items():
            if keyword in body.lower():
                category = category_value
                break

    # Return the extracted data
    if amount:
        return (amount, category, transaction_type)
    return None

# Function to process CSV and extract relevant transaction information
def process_csv(file_path, categories_mapping):
    credit_data = []
    debit_data = []
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                subject = row['subject']
                body = row['body']
                date = row['date']
                to_email = row['to']  # Use 'to' instead of 'from'
                
                result = determine_category(subject, body, categories_mapping)
                
                # Only append valid results (non-None) to the respective data lists
                if result:
                    amount, category, transaction_type = result
                    if transaction_type == 'Income':
                        credit_data.append((amount, date, category, to_email, transaction_type))
                    elif transaction_type == 'Income':
                        debit_data.append((amount, date, category, to_email, transaction_type))

    except Exception as e:
        print(f"Error processing CSV file: {e}")
    
    # Print results for Credit/Income and Debit/Expense transactions in tuple format
    print("Credit/Income Data:")
    credit_headings = ('Amount', 'Date', 'Category', 'To', 'Type')
    print(f"{credit_headings}")
    for data in credit_data:
        print(f"{data}")

    print("\nDebit/Expense Data:")
    debit_headings = ('Amount', 'Date', 'Category', 'To', 'Type')
    print(f"{debit_headings}")
    for data in debit_data:
        # Skip None values in Debit/Expense data
        if None not in data:
            print(f"{data}")

    return credit_data, debit_data

# Function to connect to SQLite database
def connect_to_db(db_name="db.sqlite3"):
    return sqlite3.connect(db_name)

# Function to get the user_id based on email
def get_user_id(cursor, email):
    cursor.execute("SELECT id FROM auth_user WHERE email = ?", (email,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else 0  # If email doesn't exist, return 0

# Function to insert data into home_addmoney_info and home_addmoney_info1
def insert_transaction_data(cursor, user_id, amount, date, category, add_money):
    # Insert data into home_addmoney_info
    cursor.execute("""
        INSERT INTO home_addmoney_info (quantity, Date, Category, user_id, add_money)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, date, category, user_id, add_money))

    # Insert data into home_addmoney_info1
    cursor.execute("""
        INSERT INTO home_addmoney_info1 (add_money, quantity, Date, Category, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (add_money, amount, date, category, user_id))

# Function to process and insert credit and debit data
def process_and_insert_data(db_name, credit_data, debit_data):
    # Establishing database connection
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    for data in credit_data:
        amount, date, category, to_email, transaction_type = data
        user_id = get_user_id(cursor, to_email)  # Fetch user_id based on "to" email
        insert_transaction_data(cursor, user_id, amount, date, category, transaction_type)

    for data in debit_data:
        amount, date, category, to_email, transaction_type = data
        user_id = get_user_id(cursor, to_email)  # Fetch user_id based on "to" email
        insert_transaction_data(cursor, user_id, amount, date, category, transaction_type)

    # Commit the transactions and close the connection
    conn.commit()

    # Fetch and print the data from the database
    cursor.execute("SELECT * FROM home_addmoney_info")
    print("\nhome_addmoney_info data:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM home_addmoney_info1")
    print("\nhome_addmoney_info1 data:")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# Example CSV processing and data insertion
categories_mapping = load_categories_mapping()
file_path = r"C:\Users\Lenova\OneDrive\Desktop\Projects\Final Sem Project\mock_email_environment\email_logs\sampleData.csv"
credit_data, debit_data = process_csv(file_path, categories_mapping)
process_and_insert_data("db.sqlite3", credit_data, debit_data)
