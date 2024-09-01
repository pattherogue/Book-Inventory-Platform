import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

def update_books_table():
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Log the current table structure
        cur.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = 'books';")
        logging.info("Current books table structure:")
        for row in cur.fetchall():
            logging.info(row)

        # Alter the table
        alter_statements = [
            "ALTER TABLE books ALTER COLUMN title TYPE VARCHAR(500)",
            "ALTER TABLE books ALTER COLUMN authors TYPE TEXT",
            "ALTER TABLE books ALTER COLUMN image_link TYPE TEXT",
            "ALTER TABLE books ALTER COLUMN description TYPE TEXT"
        ]

        for statement in alter_statements:
            logging.info(f"Executing: {statement}")
            cur.execute(statement)

        # Commit the changes
        conn.commit()

        # Log the new table structure
        cur.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = 'books';")
        logging.info("New books table structure:")
        for row in cur.fetchall():
            logging.info(row)

        logging.info("Books table updated successfully")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update_books_table()