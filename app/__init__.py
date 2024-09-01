from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging

db = SQLAlchemy()
login_manager = LoginManager()

def create_tables(app):
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"An error occurred during database table creation: {str(e)}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    from app.routes import auth_bp, books_bp, cart_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)

    return app