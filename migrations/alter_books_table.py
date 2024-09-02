from app import create_app, db
import sqlalchemy as sa
import logging

logging.basicConfig(level=logging.INFO)

app = create_app()

def upgrade():
    with app.app_context():
        try:
            conn = db.engine.connect()
            
            # Log existing table structure
            inspector = sa.inspect(db.engine)
            columns = inspector.get_columns('books')
            logging.info(f"Existing 'books' table structure: {columns}")
            
            # Alter books table
            alter_statements = [
                "ALTER TABLE books ALTER COLUMN title TYPE VARCHAR(1000)",
                "ALTER TABLE books ALTER COLUMN authors TYPE TEXT",
                "ALTER TABLE books ALTER COLUMN image_link TYPE TEXT",
                "ALTER TABLE books ALTER COLUMN description TYPE TEXT"
            ]
            
            for statement in alter_statements:
                logging.info(f"Executing: {statement}")
                conn.execute(sa.text(statement))
            
            conn.commit()
            
            # Log new table structure
            inspector = sa.inspect(db.engine)
            new_columns = inspector.get_columns('books')
            logging.info(f"New 'books' table structure: {new_columns}")
            
            logging.info("Books table altered successfully.")
        except Exception as e:
            logging.error(f"Error altering books table: {str(e)}")
            raise

if __name__ == '__main__':
    upgrade()