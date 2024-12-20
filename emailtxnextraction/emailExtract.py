import csv
import re

# Function to determine the category of the transaction
def determine_category(subject, body):
    # Check if body contains relevant keywords for credit or debit transactions
    credit_keywords = ['refund', 'credit', 'received']
    debit_keywords = ['purchase', 'paid', 'expense', 'spent', 'transfer']

    # Amount extraction pattern
    amount_pattern = r'(\$|Rs\.?)\s?(\d+[\.,]?\d*)'

    category = None
    amount = None
    transaction_type = None

    # Check for keywords in subject or body and extract amount if available
    if any(keyword in body.lower() for keyword in credit_keywords):
        category = 'Credit/Income'
        transaction_type = 'Credit/Income'
        amount_match = re.search(amount_pattern, body)
        if amount_match:
            amount = amount_match.group(2).replace(',', '')  # Remove commas for consistency
        return (amount, category, transaction_type)

    if any(keyword in body.lower() for keyword in debit_keywords):
        category = 'Debit/Expense'
        transaction_type = 'Debit/Expense'
        amount_match = re.search(amount_pattern, body)
        if amount_match:
            amount = amount_match.group(2).replace(',', '')  # Remove commas for consistency
        return (amount, category, transaction_type)

    # Return None if no relevant transaction type found
    return None

# Function to process CSV and extract relevant transaction information
def process_csv(file_path):
    credit_data = []
    debit_data = []
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                subject = row['subject']
                body = row['body']
                date = row['date']
                from_email = row['from']
                
                result = determine_category(subject, body)
                
                # Only append valid results (non-None) to the respective data lists
                if result:
                    amount, category, transaction_type = result
                    if transaction_type == 'Credit/Income':
                        credit_data.append((amount, date, category, from_email, transaction_type))
                    elif transaction_type == 'Debit/Expense':
                        debit_data.append((amount, date, category, from_email, transaction_type))

    except Exception as e:
        print(f"Error processing CSV file: {e}")
    
    # Print results for Credit/Income and Debit/Expense transactions in tuple format
    print("Credit/Income Data:")
    credit_headings = ('Amount', 'Date', 'Category', 'From', 'Type')
    print(f"{credit_headings}")
    for data in credit_data:
        print(f"{data}")

    print("\nDebit/Expense Data:")
    debit_headings = ('Amount', 'Date', 'Category', 'From', 'Type')
    print(f"{debit_headings}")
    for data in debit_data:
        # Skip None values in Debit/Expense data
        if None not in data:
            print(f"{data}")

# Replace with your actual CSV file path
file_path = r"C:\Users\Lenova\OneDrive\Desktop\Projects\Final Sem Project\mock_email_environment\email_logs\user@example.com.csv"
process_csv(file_path)

import sqlite3
from datetime import datetime

# Function to connect to SQLite database
def connect_to_db(db_name="db.sqlite3"):
    return sqlite3.connect(db_name)

# Function to get the user_id based on email
def get_user_id(cursor, email):
    cursor.execute("SELECT id FROM auth_user WHERE email = ?", (email,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None

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
        amount, date, category, from_email, transaction_type = data
        user_id = get_user_id(cursor, from_email)  # Fetch user_id based on email
        if user_id:
            add_money = "Credit"  # Example for Credit/Income
            insert_transaction_data(cursor, user_id, amount, date, category, add_money)

    for data in debit_data:
        amount, date, category, from_email, transaction_type = data
        user_id = get_user_id(cursor, from_email)  # Fetch user_id based on email
        if user_id:
            add_money = "Debit"  # Example for Debit/Expense
            insert_transaction_data(cursor, user_id, amount, date, category, add_money)

    # Commit the transactions and close the connection
    conn.commit()
    conn.close()

# Example data from Credit/Income and Debit/Expense (modify based on your data)
credit_data = [
    ('500.00', '25-12-2024 12:00', 'Credit/Income', 'mynthra@spfa.com', 'Credit/Income'),
    ('1200', '12-12-2024 00:00', 'Credit/Income', 'shop@store.com', 'Credit/Income'),
    ('50', '19-12-2024 00:00', 'Credit/Income', 'shop@store.com', 'Credit/Income'),
    ('150', '20-12-2024 00:00', 'Credit/Income', 'bob@mail.com', 'Credit/Income'),
]

debit_data = [
    ('500.00', '21-12-2024 12:00', 'Debit/Expense', 'mynthra@spfa.com', 'Debit/Expense'),
    ('1200.', '10-12-2024 00:00', 'Debit/Expense', 'customer1@mail.com', 'Debit/Expense'),
    ('200', '15-12-2024 00:00', 'Debit/Expense', 'john@mail.com', 'Debit/Expense'),
    ('100', '16-12-2024 00:00', 'Debit/Expense', 'customer1@mail.com', 'Debit/Expense'),
]

# Calling function to process and insert the data
process_and_insert_data("db.sqlite3", credit_data, debit_data)
