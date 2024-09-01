from flask import Blueprint, render_template, redirect, url_for, flash, request
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

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import CartItem, Book
from app import db
from app.services.google_books_api import get_book_details
import logging

bp = Blueprint('cart', __name__)

@bp.route('/cart/add/<book_id>')
@login_required
def add_to_cart(book_id):
    logging.info(f"Attempting to add book with ID: {book_id} to cart")
    try:
        book = Book.query.get(book_id)
        if not book:
            logging.info(f"Book not found in database, fetching from API")
            book_data = get_book_details(book_id)
            if book_data:
                logging.info(f"Book data fetched: {book_data}")
                try:
                    book = Book(
                        id=book_data['id'],
                        title=book_data['title'],
                        authors=book_data['authors'],
                        published_date=book_data['published_date'],
                        description=book_data['description'],
                        image_link=book_data['image_link']
                    )
                    db.session.add(book)
                    db.session.flush()  # This will assign an ID if it's auto-incrementing
                    logging.info(f"Book object created: {book.id}")
                except Exception as e:
                    logging.error(f"Error creating Book object: {str(e)}")
                    raise

                try:
                    db.session.commit()
                    logging.info(f"New book added to database: {book.id}")
                except Exception as commit_error:
                    db.session.rollback()
                    logging.error(f"Error committing new book to database: {str(commit_error)}")
                    raise
            else:
                logging.error(f"Book not found in API: {book_id}")
                flash('Book not found')
                return redirect(url_for('books.search'))

        try:
            cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            if cart_item:
                cart_item.quantity += 1
                logging.info(f"Increased quantity for existing cart item: {cart_item.id}")
            else:
                cart_item = CartItem(user_id=current_user.id, book_id=book_id)
                db.session.add(cart_item)
                logging.info(f"Created new cart item for user {current_user.id} and book {book_id}")
            
            db.session.commit()
            flash('Book added to cart')
            logging.info("Book successfully added to cart")
        except Exception as cart_error:
            db.session.rollback()
            logging.error(f"Error adding book to cart: {str(cart_error)}")
            raise

        return redirect(url_for('cart.view_cart'))
    except Exception as e:
        logging.error(f"Unexpected error in add_to_cart: {str(e)}")
        flash('Error adding book to database. Please try again.')
        return redirect(url_for('books.search'))




@bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Book removed from cart')
    return redirect(url_for('cart.view_cart'))

@bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        quantity = int(request.form.get('quantity', 0))
        if quantity > 0:
            cart_item.quantity = quantity
            db.session.commit()
            flash('Cart updated successfully')
        elif quantity == 0:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Item removed from cart')
        else:
            flash('Invalid quantity')
    else:
        flash('Item not found')
    return redirect(url_for('cart.view_cart'))