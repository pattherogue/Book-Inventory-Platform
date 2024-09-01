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

    with app.app_context():
        # Reflect the current database schema
        db.reflect()
        logging.info("Database schema reflected")

        # Log the current table structure
        for table_name in db.metadata.tables:
            table = db.metadata.tables[table_name]
            logging.info(f"Table: {table_name}")
            for column in table.columns:
                logging.info(f"  Column: {column.name}, Type: {column.type}")

    from app.routes import auth, books, cart, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(main.bp)

    return app