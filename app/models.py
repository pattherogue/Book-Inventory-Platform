from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['users']

    def get_id(self):
        return str(self.id)

class Book(db.Model):
    __table__ = db.Model.metadata.tables['books']

class CartItem(db.Model):
    __table__ = db.Model.metadata.tables['cart_items']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))