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
    SELECT column_name, data_type, character_maximum_length 
    FROM information_schema.columns 
    WHERE table_name = 'books';
    """
    columns = execute_sql(sql)
    logging.info("Current books table structure:")
    for column in columns:
        logging.info(f"Column: {column[0]}, Type: {column[1]}, Max Length: {column[2]}")
    return columns

def update_books_table():
    try:
        # Drop the existing books table
        execute_sql("DROP TABLE IF EXISTS books CASCADE;")
        logging.info("Dropped existing books table")

        # Create the books table with the correct structure
        create_table_sql = """
        CREATE TABLE books (
            id VARCHAR(64) PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            authors TEXT,
            published_date VARCHAR(20),
            description TEXT,
            image_link TEXT
        );
        """
        execute_sql(create_table_sql)
        logging.info("Created new books table with correct structure")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def insert_test_book():
    try:
        test_book = {
            'id': 'test123',
            'title': 'Test Book with a Very Long Title' * 10,
            'authors': 'Test Author 1, Test Author 2',
            'published_date': '2023-09-01',
            'description': 'This is a test book description.' * 100,
            'image_link': 'http://example.com/test-image.jpg' * 5
        }

        insert_sql = """
        INSERT INTO books (id, title, authors, published_date, description, image_link)
        VALUES (%(id)s, %(title)s, %(authors)s, %(published_date)s, %(description)s, %(image_link)s);
        """

        execute_sql(insert_sql, test_book)
        logging.info("Test book inserted successfully")

        # Verify the inserted data
        result = execute_sql("SELECT * FROM books WHERE id = 'test123';")
        logging.info(f"Retrieved test book: {result}")
    except Exception as e:
        logging.error(f"Error inserting test book: {str(e)}")

if __name__ == "__main__":
    logging.info("Checking initial table structure...")
    check_table_structure()
    
    logging.info("Updating table structure...")
    update_books_table()
    
    logging.info("Checking final table structure...")
    check_table_structure()

    logging.info("Inserting test book...")
    insert_test_book()

    logging.info("Final verification of table structure...")
    check_table_structure()