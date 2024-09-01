from flask import Blueprint, render_template, request
from flask_login import login_required
from app.services.google_books_api import search_books, get_book_details

bp = Blueprint('books', __name__)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        books = search_books(query)
        return render_template('books/search_results.html', books=books)
    return render_template('books/search.html')

@bp.route('/book/<book_id>')
@login_required
def book_details(book_id):
    book = get_book_details(book_id)
    return render_template('books/book_details.html', book=book)