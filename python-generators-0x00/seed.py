#!/usr/bin/python3
import mysql.connector
import csv
import uuid

# Connect to MySQL server
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # Replace with your actual password
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database if not exists
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your actual password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
        """
        cursor.execute(query)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON user_data(user_id);")
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Insert data from CSV file
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (row["user_id"], row["name"], row["email"], row["age"])
                )
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
