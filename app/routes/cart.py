from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import CartItem, Book
from app import db
from app.services.google_books_api import get_book_details

bp = Blueprint('cart', __name__)

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
                    title=book_data['title'][:500],
                    authors=book_data['authors'],
                    published_date=book_data['published_date'][:20],
                    description=book_data['description'],
                    image_link=book_data['image_link']
                )
                db.session.add(book)
                db.session.commit()
            else:
                flash('Book not found')
                return redirect(url_for('books.search'))

        cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
            db.session.add(cart_item)
        
        db.session.commit()
        flash('Book added to cart')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding book to cart: {str(e)}")
        flash('An error occurred while adding the book to the cart')
    
    return redirect(url_for('cart.view_cart'))

@bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/view.html', cart_items=cart_items)

@bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('You do not have permission to remove this item.')
        return redirect(url_for('cart.view_cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart')
    return redirect(url_for('cart.view_cart'))