from models.post import Post
from models.user import User
from data_store import DataStore
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUserClass:
    """Test cases for User class"""

    def test_user_creation(self):
        """Test User object creation"""
        user = User(id=1, name="Test User", email="test@example.com")
        assert user.id == 1
        assert user.name == "Test User"
        assert user.email == "test@example.com"

    def test_user_to_dict(self):
        """Test User to_dict method"""
        user = User(id=1, name="Test User", email="test@example.com")
        user_dict = user.to_dict()

        expected = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com"
        }
        assert user_dict == expected

    def test_user_from_dict(self):
        """Test User from_dict class method"""
        user_data = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com"
        }
        user = User.from_dict(user_data)

        assert user.id == 1
        assert user.name == "Test User"
        assert user.email == "test@example.com"


class TestPostClass:
    """Test cases for Post class"""

    def test_post_creation(self):
        """Test Post object creation"""
        post = Post(id=1, title="Test Post", content="Test content", user_id=1)
        assert post.id == 1
        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.user_id == 1

    def test_post_to_dict(self):
        """Test Post to_dict method"""
        post = Post(id=1, title="Test Post", content="Test content", user_id=1)
        post_dict = post.to_dict()

        expected = {
            "id": 1,
            "title": "Test Post",
            "content": "Test content",
            "user_id": 1
        }
        assert post_dict == expected

    def test_post_from_dict(self):
        """Test Post from_dict class method"""
        post_data = {
            "id": 1,
            "title": "Test Post",
            "content": "Test content",
            "user_id": 1
        }
        post = Post.from_dict(post_data)

        assert post.id == 1
        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.user_id == 1


class TestDataStore:
    """Test cases for DataStore class"""

    @pytest.fixture
    def fresh_data_store(self):
        """Create a fresh DataStore instance for testing"""
        return DataStore()

    def test_data_store_initialization(self, fresh_data_store):
        """Test DataStore initialization with sample data"""
        users = fresh_data_store.get_all_users()
        posts = fresh_data_store.get_all_posts()

        assert len(users) == 2  # Sample users
        assert len(posts) == 3  # Sample posts
        assert fresh_data_store._next_user_id == 3
        assert fresh_data_store._next_post_id == 4

    def test_create_user(self, fresh_data_store):
        """Test creating a new user"""
        user = fresh_data_store.create_user("New User", "new@example.com")

        assert user.name == "New User"
        assert user.email == "new@example.com"
        assert user.id == 3  # Next available ID

        # Verify user was stored
        retrieved_user = fresh_data_store.get_user(3)
        assert retrieved_user == user

    def test_get_user(self, fresh_data_store):
        """Test getting a user by ID"""
        user = fresh_data_store.get_user(1)
        assert user is not None
        assert user.name == "John Doe"

        # Test non-existent user
        user = fresh_data_store.get_user(999)
        assert user is None

    def test_get_user_by_email(self, fresh_data_store):
        """Test getting a user by email"""
        user = fresh_data_store.get_user_by_email("john@example.com")
        assert user is not None
        assert user.id == 1

        # Test non-existent email
        user = fresh_data_store.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_update_user(self, fresh_data_store):
        """Test updating a user"""
        updated_user = fresh_data_store.update_user(1, name="Updated Name")
        assert updated_user is not None
        assert updated_user.name == "Updated Name"
        assert updated_user.email == "john@example.com"  # Unchanged

        # Test updating email
        updated_user = fresh_data_store.update_user(
            1, email="updated@example.com")
        assert updated_user.email == "updated@example.com"

        # Test updating non-existent user
        updated_user = fresh_data_store.update_user(999, name="New Name")
        assert updated_user is None

    def test_delete_user(self, fresh_data_store):
        """Test deleting a user"""
        # Verify user exists
        user = fresh_data_store.get_user(1)
        assert user is not None

        # Delete user
        result = fresh_data_store.delete_user(1)
        assert result is True

        # Verify user is deleted
        user = fresh_data_store.get_user(1)
        assert user is None

        # Test deleting non-existent user
        result = fresh_data_store.delete_user(999)
        assert result is False

    def test_user_exists(self, fresh_data_store):
        """Test checking if user exists"""
        assert fresh_data_store.user_exists(1) is True
        assert fresh_data_store.user_exists(999) is False

    def test_create_post(self, fresh_data_store):
        """Test creating a new post"""
        post = fresh_data_store.create_post("New Post", "New content", 1)

        assert post is not None
        assert post.title == "New Post"
        assert post.content == "New content"
        assert post.user_id == 1
        assert post.id == 4  # Next available ID

        # Verify post was stored
        retrieved_post = fresh_data_store.get_post(4)
        assert retrieved_post == post

    def test_create_post_invalid_user(self, fresh_data_store):
        """Test creating a post with invalid user_id"""
        post = fresh_data_store.create_post("New Post", "New content", 999)
        assert post is None

    def test_get_post(self, fresh_data_store):
        """Test getting a post by ID"""
        post = fresh_data_store.get_post(1)
        assert post is not None
        assert post.title == "First Post"

        # Test non-existent post
        post = fresh_data_store.get_post(999)
        assert post is None

    def test_update_post(self, fresh_data_store):
        """Test updating a post"""
        updated_post = fresh_data_store.update_post(1, title="Updated Title")
        assert updated_post is not None
        assert updated_post.title == "Updated Title"
        assert updated_post.content == "This is the content of the first post"  # Unchanged

        # Test updating with invalid user_id
        updated_post = fresh_data_store.update_post(1, user_id=999)
        assert updated_post is None

        # Test updating non-existent post
        updated_post = fresh_data_store.update_post(999, title="New Title")
        assert updated_post is None

    def test_delete_post(self, fresh_data_store):
        """Test deleting a post"""
        # Verify post exists
        post = fresh_data_store.get_post(1)
        assert post is not None

        # Delete post
        result = fresh_data_store.delete_post(1)
        assert result is True

        # Verify post is deleted
        post = fresh_data_store.get_post(1)
        assert post is None

        # Test deleting non-existent post
        result = fresh_data_store.delete_post(999)
        assert result is False

    def test_get_posts_by_user(self, fresh_data_store):
        """Test getting posts by user ID"""
        user_posts = fresh_data_store.get_posts_by_user(1)
        assert len(user_posts) == 2  # User 1 has 2 posts

        # Test with non-existent user
        user_posts = fresh_data_store.get_posts_by_user(999)
        assert len(user_posts) == 0

    def test_delete_user_cascades_to_posts(self, fresh_data_store):
        """Test that deleting a user also deletes their posts"""
        # Verify user has posts
        user_posts = fresh_data_store.get_posts_by_user(1)
        assert len(user_posts) > 0

        # Delete user
        result = fresh_data_store.delete_user(1)
        assert result is True

        # Verify user's posts were also deleted
        user_posts_after = fresh_data_store.get_posts_by_user(1)
        assert len(user_posts_after) == 0

        # Verify posts are no longer in the store
        for post in user_posts:
            assert fresh_data_store.get_post(post.id) is None
