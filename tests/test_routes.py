import pytest
from flask_login import current_user
from app.models import User, Book, CartItem

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Book Review Platform" in response.data

def test_search_books(client):
    response = client.get('/search')
    assert response.status_code == 302  # Should redirect to login if not authenticated

def test_add_to_cart(client, init_database):
    # Login the test user
    client.post('/login', data=dict(
        username="testuser",
        password="testpassword"
    ), follow_redirects=True)

    # Add a book to the cart
    response = client.get('/cart/add/testbook1', follow_redirects=True)
    assert response.status_code == 200
    assert b"Book added to cart" in response.data

def test_view_cart(client, init_database):
    # Login the test user
    client.post('/login', data=dict(
        username="testuser",
        password="testpassword"
    ), follow_redirects=True)

    # Add a book to the cart
    client.get('/cart/add/testbook1')

    # View the cart
    response = client.get('/cart')
    assert response.status_code == 200
    assert b"Your Cart" in response.data
    assert b"Test Book" in response.data

def test_update_quantity(client, init_database):
    # Login the test user
    client.post('/login', data=dict(
        username="testuser",
        password="testpassword"
    ), follow_redirects=True)

    # Add a book to the cart
    client.get('/cart/add/testbook1')

    # Get the cart item
    with client.application.app_context():
        cart_item = CartItem.query.filter_by(user_id=1, book_id="testbook1").first()

    # Update the quantity
    response = client.post(f'/cart/update/{cart_item.id}', data=dict(
        quantity=3
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Cart updated successfully" in response.data

    # Check if the quantity was updated in the database
    with client.application.app_context():
        updated_item = CartItem.query.get(cart_item.id)
        assert updated_item.quantity == 3