import pytest
from unittest.mock import patch
from app.services.google_books_api import search_books, get_book_details

@pytest.fixture
def mock_requests_get():
    with patch('app.services.google_books_api.requests.get') as mock_get:
        yield mock_get

def test_search_books(app, mock_requests_get):
    mock_response = {
        'items': [
            {
                'id': 'book1',
                'volumeInfo': {
                    'title': 'Test Book',
                    'authors': ['Test Author'],
                    'publishedDate': '2021',
                    'description': 'A test book',
                    'imageLinks': {'thumbnail': 'http://example.com/image.jpg'}
                }
            }
        ]
    }
    mock_requests_get.return_value.json.return_value = mock_response

    with app.app_context():
        results = search_books('test query')

    assert len(results) == 1
    assert results[0]['title'] == 'Test Book'
    assert results[0]['authors'] == 'Test Author'

def test_get_book_details(app, mock_requests_get):
    mock_response = {
        'id': 'book1',
        'volumeInfo': {
            'title': 'Test Book',
            'authors': ['Test Author'],
            'publishedDate': '2021',
            'description': 'A test book',
            'imageLinks': {'thumbnail': 'http://example.com/image.jpg'},
            'pageCount': 200,
            'categories': ['Fiction'],
            'language': 'en'
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response

    with app.app_context():
        book = get_book_details('book1')

    assert book['id'] == 'book1'
    assert book['title'] == 'Test Book'
    assert book['authors'] == 'Test Author'
    assert book['page_count'] == 200
    assert book['categories'] == 'Fiction'
    assert book['language'] == 'en'