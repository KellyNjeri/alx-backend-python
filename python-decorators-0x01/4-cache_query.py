import time
import sqlite3 
import functools
import hashlib

# Reuse the with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection as first argument if not already provided
            if 'conn' not in kwargs and not (args and isinstance(args[0], sqlite3.Connection)):
                result = func(conn, *args, **kwargs)
            else:
                result = func(*args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Create a cache key based on the query
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[cache_key]
        
        # Execute query and cache result
        print(f"Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # Create test database and table
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
    conn.commit()
    conn.close()
    
    # First call will cache the result
    print("First call:")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Users: {users}")
    
    # Second call will use the cached result
    print("\nSecond call:")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Users (cached): {users_again}")