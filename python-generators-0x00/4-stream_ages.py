import mysql.connector
from mysql.connector import Error
from typing import Generator, Optional
from mysql.connector.connection import MySQLConnection

def connect_to_prodev() -> Optional[MySQLConnection]:
    """Connect to the ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def stream_user_ages() -> Generator[int, None, None]:
    """Generator that yields user ages one by one"""
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            if row[0] is not None:  # Skip NULL values
                yield int(row[0])
            
    except Error as e:
        print(f"Error streaming ages: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()

def calculate_average_age() -> None:
    """Calculate average age using the generator"""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found")

if __name__ == "__main__":
    calculate_average_age()
