from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import CartItem, Book
from app import db
from app.services.google_books_api import get_book_details
from sqlalchemy.exc import IntegrityError
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
    logging.info(f"Attempting to add book with ID: {book_id} to cart")
    try:
        book_data = get_book_details(book_id)
        if book_data:
            logging.info(f"Book data fetched: {book_data}")
        else:
            logging.error(f"Book not found in API: {book_id}")
        
        logging.info(f"User ID: {current_user.id}")
        logging.info(f"Book ID: {book_id}")
        
        flash('Book data logged (not added to cart)')
        return redirect(url_for('books.search'))
    except Exception as e:
        logging.error(f"Unexpected error in add_to_cart: {str(e)}")
        logging.error(f"Full traceback: ", exc_info=True)
        flash('An unexpected error occurred. Please try again.')
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