from app import create_app, db
from app.models import User, Book, CartItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'CartItem': CartItem}

if __name__ == '__main__':
    app.run(debug=True)