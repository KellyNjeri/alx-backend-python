import mysql.connector
import csv
from mysql.connector import Error
from typing import Optional

def connect_db() -> Optional[mysql.connector.connection.MySQLConnection]:
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change if needed
            password=''   # Change if needed
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev() -> Optional[mysql.connector.connection.MySQLConnection]:
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',      # Change if needed
            password='',      # Change if needed
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the user_data table if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        print("Table user_data created successfully")
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection: mysql.connector.connection.MySQLConnection, csv_file: str) -> None:
    """Insert data from CSV file into the database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Data already exists in the table")
            return

        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            data_to_insert = []

            for row in csv_reader:
                if len(row) == 4 and row[3].isdigit():  # Validate age
                    data_to_insert.append((row[0], row[1], row[2], int(row[3])))

            cursor.executemany(
                "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                data_to_insert
            )

        connection.commit()
        print(f"{cursor.rowcount} rows inserted successfully")
        cursor.close()

    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
