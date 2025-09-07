import mysql.connector
from mysql.connector import Error
from typing import Generator, Dict, Any, List, Optional
import seed  # Import the seed module for connect_to_prodev function

def paginate_users(page_size: int, offset: int) -> List[Dict[str, Any]]:
    """Fetch a page of users from the database"""
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error paginating users: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        connection.close()

def lazy_pagination(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """Generator that lazily loads each page of users"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size