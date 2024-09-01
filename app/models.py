from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['users']

class Book(db.Model):
    __table__ = db.Model.metadata.tables['books']

class CartItem(db.Model):
    __table__ = db.Model.metadata.tables['cart_items']