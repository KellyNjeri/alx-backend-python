# Python Generators Project

This project demonstrates advanced usage of Python generators for efficient data processing with large datasets.

## Features

- Database setup and seeding with user data
- Stream processing of database rows
- Batch processing with filtering
- Lazy pagination of large datasets
- Memory-efficient aggregation using generators

## Setup

1. Install MySQL and ensure it's running
2. Install required dependencies:
   ```bash
   pip install mysql-connector-python

   python -c "import seed; seed.insert_data(seed.connect_to_prodev(), 'user_data.csv')"

## Usage

0-stream_users.py: Stream users one by one

1-batch_processing.py: Process users in batches

2-lazy_paginate.py: Lazy pagination of users

4-stream_ages.py: Memory-efficient age calculation

## Database Schema
The project uses a MySQL database ALX_prodev with table user_data containing:

user_id (VARCHAR(36), PRIMARY KEY)

name (VARCHAR(255), NOT NULL)

email (VARCHAR(255), NOT NULL)

age (DECIMAL(3,0), NOT NULL)


## Important Notes:

1. **Database Configuration**: You may need to modify the database connection parameters in each file based on your MySQL setup.

2. **CSV File**: Make sure the `user_data.csv` file is in the same directory as the scripts.

3. **Dependencies**: Install the MySQL connector with `pip install mysql-connector-python`.

4. **Database Setup**: Run the seed script first to create the database and populate it with data.

This implementation follows all the requirements:
- Uses generators with `yield` for memory efficiency
- Implements batch processing and lazy loading
- Handles database connections properly
- Uses no more than the specified number of loops
- Provides memory-efficient aggregation without using SQL AVG