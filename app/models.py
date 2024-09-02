from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def get_id(self):
        return str(self.id)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)
    published_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    image_link = db.Column(db.Text)

    @classmethod
    def create_or_update(cls, book_data):
        try:
            book = cls.query.filter_by(id=book_data['id']).with_for_update().one()
            # Update existing book
            for key, value in book_data.items():
                setattr(book, key, value)
        except NoResultFound:
            # Create new book
            book = cls(**book_data)
            db.session.add(book)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # If commit failed, try to get the book again (it might have been inserted by another process)
            book = cls.query.filter_by(id=book_data['id']).one()
        
        return book

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(64), db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    book = relationship('Book', backref='cart_items')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))