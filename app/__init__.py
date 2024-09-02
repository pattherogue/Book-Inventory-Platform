from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import logging

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'

    from app.routes import auth, books, cart, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(main.bp)

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