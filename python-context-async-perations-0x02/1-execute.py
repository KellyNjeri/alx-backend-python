import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Create test data
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                         (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        cursor.execute("DELETE FROM users")  # Clear existing data
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)", ())
        cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)", ())
        cursor.execute("INSERT INTO users (name, age) VALUES ('Charlie', 35)", ())
        cursor.execute("INSERT INTO users (name, age) VALUES ('David', 40)", ())
        cursor.execute("INSERT INTO users (name, age) VALUES ('Eve', 28)", ())
        conn.commit()
    
    # Use the context manager with parameterized query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery('test.db', query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)