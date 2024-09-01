from app import create_app, db
from app.models import User, Book, CartItem
import logging
import sqlalchemy as sa

logging.basicConfig(level=logging.INFO)

app = create_app()

def create_tables_if_not_exist():
    with app.app_context():
        inspector = sa.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        for model in [User, Book, CartItem]:
            if model.__tablename__ not in existing_tables:
                model.__table__.create(db.engine)
                logging.info(f"Created table for {model.__name__}")
            else:
                logging.info(f"Table for {model.__name__} already exists")

if __name__ == '__main__':
    create_tables_if_not_exist()
    print("Database initialization complete.")