from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from dotenv import load_dotenv

load_dotenv()  # This line loads the environment variables from .env

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import auth, books, cart
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp)

    return app