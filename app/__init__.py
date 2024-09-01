from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging
import sqlalchemy as sa

db = SQLAlchemy()
login_manager = LoginManager()

def create_tables(app):
    with app.app_context():
        try:
            # Test database connection
            with db.engine.connect() as conn:
                logging.info("Successfully connected to the database.")
            
            # Get existing tables
            inspector = sa.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            logging.info(f"Existing tables before creation: {existing_tables}")
            
            # Import models
            from app.models import User, Book, CartItem
            
            # Try to create each table individually
            for model in [User, Book, CartItem]:
                try:
                    model.__table__.create(db.engine)
                    logging.info(f"Table for {model.__name__} created successfully")
                except Exception as table_error:
                    logging.error(f"Error creating table for {model.__name__}: {str(table_error)}")
            
            # Check tables again
            inspector = sa.inspect(db.engine)
            new_tables = inspector.get_table_names()
            logging.info(f"Tables after creation attempt: {new_tables}")
            
        except Exception as e:
            logging.error(f"An error occurred during database operations: {str(e)}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import auth, books, cart, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp, url_prefix='/cart')
    app.register_blueprint(main.bp)

    return app