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

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Log the database URI (make sure to remove any sensitive information)
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')
    logging.info(f"Database URI: {db_uri.split('@')[-1] if '@' in db_uri else db_uri}")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Create tables
    create_tables(app)

    from app.routes import auth_bp, books_bp, cart_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)

    logging.info("Application created and configured successfully")

    return app