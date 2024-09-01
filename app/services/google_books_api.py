import requests
from flask import current_app

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
        'title': volume_info.get('title', 'Unknown')[:500],  # Limit to 500 characters
        'authors': ', '.join(volume_info.get('authors', ['Unknown']))[:200],  # Limit to 200 characters
        'published_date': volume_info.get('publishedDate', 'Unknown')[:20],  # Limit to 20 characters
        'description': volume_info.get('description', 'No description available')[:5000],  # Limit to 5000 characters
        'image_link': volume_info.get('imageLinks', {}).get('thumbnail', '')[:500]  # Limit to 500 characters
    }