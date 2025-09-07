import mysql.connector
from mysql.connector import Error
from typing import Generator, Dict, Any

def connect_to_prodev() -> Any:
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def stream_users() -> Generator[Dict[str, Any], None, None]:
    """Generator that streams rows from user_data table one by one"""
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()