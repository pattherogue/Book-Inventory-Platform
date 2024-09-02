from flask import Blueprint, render_template, redirect, url_for, flash, request
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
    try:
        book = Book.query.get(book_id)
        if not book:
            book_data = get_book_details(book_id)
            if book_data:
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
            else:
                flash('Book not found', 'error')
                return redirect(url_for('books.search'))

        cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, book_id=book_id)
            db.session.add(cart_item)
        
        db.session.commit()
        flash('Book added to cart successfully', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding book to cart: {str(e)}")
        flash('An error occurred while adding the book to the cart', 'error')
    
    return redirect(url_for('books.search'))

@bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Book removed from cart', 'success')
    else:
        flash('Item not found', 'error')
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
            flash('Cart updated successfully', 'success')
        elif quantity == 0:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Item removed from cart', 'success')
        else:
            flash('Invalid quantity', 'error')
    else:
        flash('Item not found', 'error')
    return redirect(url_for('cart.view_cart'))