from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    image_link = db.Column(db.Text)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.String(64), db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    book = db.relationship('Book', backref=db.backref('cart_items', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))