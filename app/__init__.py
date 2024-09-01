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
        db.reflect()  # This will load the existing table structures
        from app import models  # Import models after reflecting

    from app.routes import auth, books, cart, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(main.bp)

    return app