import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.environ.get('DATABASE_URL')

def check_table_structure():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = 'books';")
        columns = cur.fetchall()
        
        logging.info("Current books table structure:")
        for column in columns:
            logging.info(f"Column: {column[0]}, Type: {column[1]}, Max Length: {column[2]}")
        
        conn.close()
    except Exception as e:
        logging.error(f"Error checking table structure: {str(e)}")

def update_books_table():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Drop the existing books table
        cur.execute("DROP TABLE IF EXISTS books CASCADE;")
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
        cur.execute(create_table_sql)
        logging.info("Created new books table with correct structure")

        conn.commit()
        logging.info("Books table updated successfully")
        conn.close()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def insert_test_book():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        test_book = {
            'id': 'test123',
            'title': 'Test Book with a Very Long Title' * 10,  # This will be longer than 200 characters
            'authors': 'Test Author 1, Test Author 2',
            'published_date': '2023-09-01',
            'description': 'This is a test book description.' * 100,  # This will be a long description
            'image_link': 'http://example.com/test-image.jpg' * 5  # This will be a long URL
        }

        insert_sql = """
        INSERT INTO books (id, title, authors, published_date, description, image_link)
        VALUES (%(id)s, %(title)s, %(authors)s, %(published_date)s, %(description)s, %(image_link)s);
        """

        cur.execute(insert_sql, test_book)
        conn.commit()
        logging.info("Test book inserted successfully")

        # Verify the inserted data
        cur.execute("SELECT * FROM books WHERE id = 'test123';")
        result = cur.fetchone()
        logging.info(f"Retrieved test book: {result}")

        conn.close()
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