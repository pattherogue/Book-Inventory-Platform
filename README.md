# Book Inventory Platform

Welcome to the Book Inventory Platform! This application allows users to manage their book collections and shopping carts. Below you'll find instructions on how to set up and run the project locally, as well as information about the deployed application.

## Deployed Application

You can access the live application at: [https://book-inventory-platform.onrender.com](https://book-inventory-platform.onrender.com)

## Getting Started

To run the project locally, follow these steps:

### Prerequisites

- Python 3.11.4 or later
- Pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repository-url.git
    cd your-repository-directory
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. Start the application:

    ```bash
    gunicorn run:app
    ```

### Environment Variables

Ensure you have the following environment variables set:

- `SECRET_KEY`: A secret key for session management. Can be generated automatically.
- `GOOGLE_BOOKS_API_KEY`: Your Google Books API key.
- `DATABASE_URL`: The connection string for your database, provided by Render.

### Database Schema

Below is a screenshot of the current database schema:

![Database Schema](https://i.imgur.com/E48gBqL.png)

## Deployment

This project is deployed using Render. The `render.yaml` configuration file used for deployment is as follows:

```yaml
services:
  - type: web
    name: book-inventory-platform
    env: python
    buildCommand: |
      pip install -r requirements.txt
      flask db init
      flask db migrate
      flask db upgrade
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.4
      - key: SECRET_KEY
        generateValue: true
      - key: GOOGLE_BOOKS_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: book_inventory_db
          property: connectionString

databases:
  - name: book_inventory_db
    databaseName: book_inventory
    user: book_inventory
```

## Contributing

Feel free to submit issues or pull requests to improve the project. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
