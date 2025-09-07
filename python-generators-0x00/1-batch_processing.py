import mysql.connector
from mysql.connector import Error
from typing import Generator, Dict, Any, List, Optional

def connect_to_prodev() -> Optional[mysql.connector.connection.MySQLConnection]:
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

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """Generator that fetches rows in batches"""
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = None
    offset = 0
    try:
        cursor = connection.cursor(dictionary=True)
        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size
    except Error as e:
        print(f"Error streaming batches: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()

def batch_processing(batch_size: int) -> None:
    """Process each batch to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)