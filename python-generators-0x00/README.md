Python Generators Project: Efficient Data Handling
This project delves into the advanced usage of Python generators, focusing on their application for efficiently handling large datasets, processing data in batches, and simulating real-world scenarios involving live updates and memory-efficient computations. The core of these tasks revolves around leveraging Python’s yield keyword to implement generators that provide iterative access to data, promoting optimal resource utilization and improving performance in data-driven applications.

Learning Objectives
By completing this project, you will:

Master Python Generators: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.

Handle Large Datasets: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.

Simulate Real-world Scenarios: Develop solutions to simulate live data updates and apply them to streaming contexts.

Optimize Performance: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.

Apply SQL Knowledge: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

Requirements
Proficiency in Python 3.x.

Understanding of yield and Python’s generator functions.

Familiarity with SQL and database operations (MySQL and SQLite).

Basic knowledge of database schema design and data seeding.

Ability to use Git and GitHub for version control and submission.

Project Structure
The project is organized into tasks, with each task building upon the previous one to demonstrate different aspects and applications of Python generators.

Task 0: Getting Started with Python Generators - Database Setup and Seeding
Objective: Create a generator that streams rows from an SQL database one by one. This initial task focuses on setting up the necessary database infrastructure.

Instructions
Database Setup:

Set up a MySQL database named ALX_prodev.

Create a table user_data within ALX_prodev with the following fields:

user_id (Primary Key, UUID, Indexed, VARCHAR(36))

name (VARCHAR, NOT NULL)

email (VARCHAR, NOT NULL)

age (INT, NOT NULL)

Data Population:

Populate the user_data table with sample data from the provided user_data.csv file.

Files
seed.py: Contains functions to connect to the MySQL database, create the database and table, and insert data from the CSV file.

0-main.py: A script to demonstrate the usage of the functions in seed.py for database setup and data insertion.

user_data.csv: The CSV file containing the sample user data.

Prototypes
The seed.py script implements the following functions:

def connect_db(): Connects to the MySQL database server.

def create_database(connection): Creates the database ALX_prodev if it does not exist.

def connect_to_prodev(): Connects to the ALX_prodev database in MySQL.

def create_table(connection): Creates a table user_data if it does not exist with the required fields.

def insert_data(connection, data): Inserts data into the database if it does not exist.

Setup and Usage
Install MySQL Connector:

pip install mysql-connector-python

MySQL Credentials:
Ensure your MySQL server is running. Open seed.py and replace "your_mysql_user" and "your_mysql_password" with your actual MySQL database credentials.

Place user_data.csv:
Make sure the user_data.csv file is in the same directory as seed.py.

Run the setup script:
Execute 0-main.py to set up the database and populate it with data.

./0-main.py

Example Output
connection successful
Connected to ALX_prodev database successfully!
Table user_data created successfully
Data inserted successfully from CSV.
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]
