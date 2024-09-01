import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.environ.get('DATABASE_URL')

def execute_sql(sql, params=None):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        conn.commit()
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def check_table_structure():
    sql = """
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public';
    """
    tables = execute_sql(sql)
    logging.info(f"Existing tables: {tables}")

def create_tables_if_not_exist():
    tables = {
        'users': """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(64) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(128)
        );
        """,
        'books': """
        CREATE TABLE IF NOT EXISTS books (
            id VARCHAR(64) PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            authors TEXT,
            published_date VARCHAR(20),
            description TEXT,
            image_link TEXT
        );
        """,
        'cart_items': """
        CREATE TABLE IF NOT EXISTS cart_items (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            book_id VARCHAR(64) REFERENCES books(id),
            quantity INTEGER DEFAULT 1
        );
        """
    }

    for table_name, create_sql in tables.items():
        try:
            execute_sql(create_sql)
            logging.info(f"Table {table_name} created or already exists")
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {str(e)}")

if __name__ == "__main__":
    logging.info("Checking initial table structure...")
    check_table_structure()
    
    logging.info("Creating tables if they don't exist...")
    create_tables_if_not_exist()
    
    logging.info("Checking final table structure...")
    check_table_structure()