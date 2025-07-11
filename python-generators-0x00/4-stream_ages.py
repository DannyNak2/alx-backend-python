#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields one user age at a time from the DB"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()

def calculate_average_age():
    """Uses a generator to calculate average age efficiently"""
    total = 0
    count = 0
    for age in stream_user_ages():  # 1st and only loop
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
