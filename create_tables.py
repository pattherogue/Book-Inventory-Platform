from app import create_app, db, create_tables
from app.models import User, Book, CartItem
import logging

logging.basicConfig(level=logging.INFO)

app = create_app()

with app.app_context():
    # Check if tables exist
    inspector = db.inspect(db.engine)
    existing_tables = inspector.get_table_names()
    logging.info(f"Existing tables: {existing_tables}")

    # Create tables
    create_tables(app)

    # Check tables again
    inspector = db.inspect(db.engine)
    new_tables = inspector.get_table_names()
    logging.info(f"Tables after creation: {new_tables}")

    # Verify each model's table
    for model in [User, Book, CartItem]:
        if model.__tablename__ in new_tables:
            logging.info(f"Table for {model.__name__} created successfully")
        else:
            logging.error(f"Table for {model.__name__} not found")

print("Database initialization complete.")