import requests
from flask import current_app

def search_books(query, max_results=10):
    api_key = current_app.config['GOOGLE_BOOKS_API_KEY']
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}&key={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    books = []
    for item in data.get('items', []):
        volume_info = item.get('volumeInfo', {})
        books.append({
            'id': item['id'],
            'title': volume_info.get('title', 'Unknown'),
            'authors': ', '.join(volume_info.get('authors', ['Unknown'])),
            'published_date': volume_info.get('publishedDate', 'Unknown'),
            'description': volume_info.get('description', 'No description available'),
            'image_link': volume_info.get('imageLinks', {}).get('thumbnail', '')
        })
    
    return books

def get_book_details(book_id):
    api_key = current_app.config['GOOGLE_BOOKS_API_KEY']
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'error' in data:
        return None

    volume_info = data.get('volumeInfo', {})
    
    return {
        'id': data['id'],
        'title': volume_info.get('title', 'Unknown'),
        'authors': ', '.join(volume_info.get('authors', ['Unknown'])),
        'published_date': volume_info.get('publishedDate', 'Unknown'),
        'description': volume_info.get('description', 'No description available'),
        'image_link': volume_info.get('imageLinks', {}).get('thumbnail', '')
    }