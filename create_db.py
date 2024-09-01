from app import create_app, db
from app.models import User, Book, CartItem
import logging
import sqlalchemy as sa

logging.basicConfig(level=logging.INFO)

app = create_app()

with app.app_context():
    try:
        # Test connection
        with db.engine.connect() as conn:
            logging.info("Successfully connected to the database.")
        
        # Get existing tables
        inspector = sa.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        logging.info(f"Existing tables before creation: {existing_tables}")
        
        # Create tables using SQL
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(64) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS books (
                id VARCHAR(64) PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                authors VARCHAR(200),
                published_date VARCHAR(20),
                description TEXT,
                image_link VARCHAR(200)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cart_items (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                book_id VARCHAR(64) REFERENCES books(id),
                quantity INTEGER DEFAULT 1
            )
            """
        ]
        
        with db.engine.connect() as conn:
            for table_sql in tables:
                conn.execute(sa.text(table_sql))
            conn.commit()
        
        logging.info("All tables created successfully")
    except Exception as e:
        logging.error(f"Error creating tables: {str(e)}")

    # Verify tables
    inspector = sa.inspect(db.engine)
    tables = inspector.get_table_names()
    logging.info(f"Existing tables after creation: {tables}")

    for model in [User, Book, CartItem]:
        if model.__tablename__ in tables:
            logging.info(f"Table for {model.__name__} exists")
        else:
            logging.error(f"Table for {model.__name__} not found")