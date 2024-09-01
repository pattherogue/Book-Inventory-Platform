from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cart = db.relationship('CartItem', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    __table__ = db.Model.metadata.tables['books']

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)
        if isinstance(self.authors, list):
            self.authors = ', '.join(self.authors)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.String(64), db.ForeignKey('books.id'))
    quantity = db.Column(db.Integer, default=1)
    book = db.relationship('Book')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))