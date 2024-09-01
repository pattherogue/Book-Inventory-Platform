from app import create_app, db, create_tables
from app.models import User, Book, CartItem

app = create_app()
create_tables(app)

print("Database tables created successfully.")