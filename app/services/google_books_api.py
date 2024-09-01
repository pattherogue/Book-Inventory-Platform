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
        volume_info = item.get('volumeInfo', {})
        book = {
            'id': item['id'],
            'title': volume_info.get('title', 'Unknown'),
            'authors': ', '.join(volume_info.get('authors', ['Unknown'])),
            'published_date': volume_info.get('publishedDate', 'Unknown'),
            'description': volume_info.get('description', 'No description available'),
            'image_link': volume_info.get('imageLinks', {}).get('thumbnail', '')
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
    
    if 'error' in data:
        return None

    volume_info = data.get('volumeInfo', {})
    
    book = {
        'id': data['id'],
        'title': volume_info.get('title', 'Unknown'),
        'authors': ', '.join(volume_info.get('authors', ['Unknown'])),
        'published_date': volume_info.get('publishedDate', 'Unknown'),
        'description': volume_info.get('description', 'No description available'),
        'image_link': volume_info.get('imageLinks', {}).get('thumbnail', ''),
        'page_count': volume_info.get('pageCount', 'Unknown'),
        'categories': ', '.join(volume_info.get('categories', ['Uncategorized'])),
        'language': volume_info.get('language', 'Unknown')
    }
    
    return book