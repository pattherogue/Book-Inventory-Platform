import pytest
from app.models import User, Book, CartItem

def test_new_user(app):
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("testpassword")
        assert user.username == "testuser"
        assert user.email == "test@test.com"
        assert user.check_password("testpassword")

def test_new_book(app):
    with app.app_context():
        book = Book(id="testbook", title="Test Book", authors="Test Author")
        assert book.id == "testbook"
        assert book.title == "Test Book"
        assert book.authors == "Test Author"

def test_cart_item(app, init_database):
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        book = Book.query.filter_by(id="testbook1").first()
        cart_item = CartItem(user_id=user.id, book_id=book.id, quantity=2)
        assert cart_item.user_id == user.id
        assert cart_item.book_id == book.id
        assert cart_item.quantity == 2