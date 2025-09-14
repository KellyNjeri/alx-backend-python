import sqlite3 
import functools

# Reuse the with_db_connection decorator from previous task
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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Updated email for user {user_id} to {new_email}")

# Example usage
if __name__ == "__main__":
    # Create test database and table
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
    conn.commit()
    conn.close()
    
    # Update user's email with automatic transaction handling 
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    
    # Verify the update
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = 1")
    user = cursor.fetchone()
    print(f"Updated user: {user}")
    conn.close()