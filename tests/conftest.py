import pytest
from app import create_app, db
from app.models import User, Book, CartItem

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpassword")
        db.session.add(user)

        # Create a test book
        book = Book(id="testbook1", title="Test Book", authors="Test Author")
        db.session.add(book)

        db.session.commit()

    yield db  # this is where the testing happens

    with app.app_context():
        db.drop_all()