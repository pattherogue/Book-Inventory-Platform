from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.exc import IntegrityError

class User(UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['users']

    def get_id(self):
        return str(self.id)

class Book(db.Model):
    __table__ = db.Model.metadata.tables['books']

    @classmethod
    def create_or_update(cls, book_data):
        book = cls.query.get(book_data['id'])
        if book is None:
            book = cls(**book_data)
            db.session.add(book)
        else:
            for key, value in book_data.items():
                setattr(book, key, value)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return book

class CartItem(db.Model):
    __table__ = db.Model.metadata.tables['cart_items']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))