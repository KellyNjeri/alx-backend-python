import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect('test.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect('test.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """Run both queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

async def setup_database():
    """Setup test database with sample data"""
    async with aiosqlite.connect('test.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        await db.execute("DELETE FROM users")  # Clear existing data
        
        # Insert test data
        users = [
            ('Alice', 30),
            ('Bob', 25),
            ('Charlie', 35),
            ('David', 45),
            ('Eve', 28),
            ('Frank', 50),
            ('Grace', 22)
        ]
        
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        await db.commit()

if __name__ == "__main__":
    # Setup database first
    asyncio.run(setup_database())
    
    # Run concurrent queries
    print("Running concurrent database queries...")
    results = asyncio.run(fetch_concurrently())
    print("All queries completed!")