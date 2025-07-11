#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields users from the database in batches"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ Using yield, not return

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def batch_processing(batch_size):
    """Filters and prints users over age 25 from streamed batches"""
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        for user in batch:  # 2nd loop
            if user["age"] > 25:
                yield user  # ✅ Must use yield (NOT return)
