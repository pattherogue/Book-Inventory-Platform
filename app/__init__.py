from flask import Flask, jsonify
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
        db.reflect()  # This will load the existing table structures
        
        # Log table structures
        for table_name in db.metadata.tables:
            table = db.metadata.tables[table_name]
            logging.info(f"Table: {table_name}")
            for column in table.columns:
                logging.info(f"  Column: {column.name}, Type: {column.type}")
            for constraint in table.constraints:
                logging.info(f"  Constraint: {constraint}")

        # Import models after reflecting
        from app import models

    # Register blueprints
    from app.routes import auth, books, cart, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(main.bp)

    @app.route('/test_db')
    def test_db():
        try:
            db.session.execute('SELECT 1')
            return 'Database connection successful!'
        except Exception as e:
            return f'Database connection failed: {str(e)}'

    @app.route('/db_schema')
    def db_schema():
        schema = []
        for table_name in db.metadata.tables:
            table = db.metadata.tables[table_name]
            table_info = {
                'name': table_name,
                'columns': [{'name': column.name, 'type': str(column.type)} for column in table.columns],
                'constraints': [str(constraint) for constraint in table.constraints]
            }
            schema.append(table_info)
        return jsonify(schema)

    return app