from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class User(UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['users']

    def get_id(self):
        return str(self.id)

class Book(db.Model):
    __table__ = db.Model.metadata.tables['books']

    @classmethod
    def create_or_update(cls, book_data):
        try:
            book = cls.query.filter_by(id=book_data['id']).one()
            # Update existing book
            for key, value in book_data.items():
                setattr(book, key, value)
        except NoResultFound:
            # Create new book
            book = cls(**book_data)
            db.session.add(book)
        
        db.session.commit()
        return book

class CartItem(db.Model):
    __table__ = db.Model.metadata.tables['cart_items']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))