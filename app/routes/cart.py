from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import CartItem, Book
from app import db
from app.services.google_books_api import get_book_details
import logging

bp = Blueprint('cart', __name__)

@bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/view.html', cart_items=cart_items)

@bp.route('/cart/add/<book_id>')
@login_required
def add_to_cart(book_id):
    logging.info(f"Attempting to add book with ID: {book_id}")
    book = Book.query.get(book_id)
    if not book:
        logging.info(f"Book not found in database, fetching from API")
        book_data = get_book_details(book_id)
        if book_data:
            logging.info(f"Book data fetched: {book_data}")
            book = Book(
                id=book_data['id'],
                title=book_data['title'],
                authors=book_data['authors'],
                published_date=book_data['published_date'],
                description=book_data['description'],
                image_link=book_data['image_link']
            )
            db.session.add(book)
            db.session.commit()
            logging.info(f"New book added to database: {book.id}")
        else:
            logging.error(f"Book not found in API: {book_id}")
            flash('Book not found')
            return redirect(url_for('books.search'))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if cart_item:
        cart_item.quantity += 1
        logging.info(f"Increased quantity for existing cart item: {cart_item.id}")
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=book_id)
        logging.info(f"Created new cart item for user {current_user.id} and book {book_id}")
    db.session.add(cart_item)
    db.session.commit()
    flash('Book added to cart')
    return redirect(url_for('cart.view_cart'))

@bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Book removed from cart')
    return redirect(url_for('cart.view_cart'))