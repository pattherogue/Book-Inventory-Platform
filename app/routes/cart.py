from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import CartItem, Book
from app import db

bp = Blueprint('cart', __name__)

@bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/view.html', cart_items=cart_items)

@bp.route('/cart/add/<book_id>')
@login_required
def add_to_cart(book_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        book = Book.query.get(book_id)
        if not book:
            flash('Book not found')
            return redirect(url_for('books.search'))
        cart_item = CartItem(user_id=current_user.id, book_id=book_id)
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