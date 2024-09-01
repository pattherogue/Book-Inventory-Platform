import requests
from flask import current_app

def search_books(query, max_results=10):
    api_key = current_app.config['GOOGLE_BOOKS_API_KEY']
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    
    params = {
        'q': query,
        'key': api_key,
        'maxResults': max_results
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    books = []
    for item in data.get('items', []):
        book = {
            'id': item['id'],
            'title': item['volumeInfo'].get('title', 'Unknown'),
            'authors': ', '.join(item['volumeInfo'].get('authors', ['Unknown'])),
            'published_date': item['volumeInfo'].get('publishedDate', 'Unknown'),
            'description': item['volumeInfo'].get('description', 'No description available'),
            'image_link': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
        }
        books.append(book)
    
    return books

def get_book_details(book_id):
    api_key = current_app.config['GOOGLE_BOOKS_API_KEY']
    base_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    
    params = {
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    book = {
        'id': data['id'],
        'title': data['volumeInfo'].get('title', 'Unknown'),
        'authors': ', '.join(data['volumeInfo'].get('authors', ['Unknown'])),
        'published_date': data['volumeInfo'].get('publishedDate', 'Unknown'),
        'description': data['volumeInfo'].get('description', 'No description available'),
        'image_link': data['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
        'page_count': data['volumeInfo'].get('pageCount', 'Unknown'),
        'categories': ', '.join(data['volumeInfo'].get('categories', ['Uncategorized'])),
        'language': data['volumeInfo'].get('language', 'Unknown')
    }
    
    return book