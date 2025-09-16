import pytest
from app import app
from data_store import data_store


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_post_data():
    """Sample post data for testing"""
    return {
        "title": "Test Post",
        "content": "This is a test post content",
        "user_id": 1
    }


@pytest.fixture(autouse=True)
def reset_data_store():
    """Reset the data store before each test"""
    # Clear existing data
    data_store._users.clear()
    data_store._posts.clear()
    data_store._next_user_id = 1
    data_store._next_post_id = 1

    # Reinitialize with sample data
    data_store._initialize_sample_data()

    yield

    # Cleanup after test
    data_store._users.clear()
    data_store._posts.clear()
    data_store._next_user_id = 1
    data_store._next_post_id = 1
