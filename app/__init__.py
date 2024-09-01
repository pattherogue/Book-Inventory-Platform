from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        try:
            # Import models here to ensure they're registered with SQLAlchemy
            from app.models import User, Book, CartItem
            
            # Check if tables exist, if not create them
            if not db.engine.has_table('user'):
                logging.info("Creating database tables...")
                db.create_all()
                logging.info("Database tables created successfully")
            else:
                logging.info("Database tables already exist")
        except Exception as e:
            logging.error(f"An error occurred during database initialization: {str(e)}")

    from app.routes import auth_bp, books_bp, cart_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)

    return app