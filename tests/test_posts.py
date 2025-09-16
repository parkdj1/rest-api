from data_store import data_store
import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPostsEndpoints:
    """Test cases for /api/posts endpoints"""

    def test_get_all_posts_success(self, client):
        """Test GET /api/posts returns all posts"""
        response = client.get('/api/posts/')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3  # Sample data has 3 posts
        assert all('id' in post for post in data)
        assert all('title' in post for post in data)
        assert all('content' in post for post in data)
        assert all('user_id' in post for post in data)

    def test_get_post_success(self, client):
        """Test GET /api/posts/<id> returns specific post"""
        response = client.get('/api/posts/1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['title'] == "First Post"
        assert data['content'] == "This is the content of the first post"
        assert data['user_id'] == 1

    def test_get_post_not_found(self, client):
        """Test GET /api/posts/<id> returns 404 for non-existent post"""
        response = client.get('/api/posts/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "Post not found"

    def test_create_post_success(self, client, sample_post_data):
        """Test POST /api/posts creates new post successfully"""
        response = client.post(
            '/api/posts/',
            data=json.dumps(sample_post_data),
            content_type='application/json'
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['title'] == sample_post_data['title']
        assert data['content'] == sample_post_data['content']
        assert data['user_id'] == sample_post_data['user_id']
        assert 'id' in data

        # Verify post was actually created
        post = data_store.get_post(data['id'])
        assert post is not None
        assert post.title == sample_post_data['title']

    def test_create_post_missing_data(self, client):
        """Test POST /api/posts returns 400 for missing required fields"""
        # Missing title
        response = client.post(
            '/api/posts/',
            data=json.dumps({"content": "Test content", "user_id": 1}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Validation failed" in data['error']
        assert 'title' in data['details']

        # Missing content
        response = client.post(
            '/api/posts/',
            data=json.dumps({"title": "Test title", "user_id": 1}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Validation failed" in data['error']
        assert 'content' in data['details']

        # Missing user_id
        response = client.post(
            '/api/posts/',
            data=json.dumps(
                {"title": "Test title", "content": "Test content"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Validation failed" in data['error']
        assert 'user_id' in data['details']

    def test_create_post_empty_data(self, client):
        """Test POST /api/posts returns 400 for empty data"""
        response = client.post(
            '/api/posts/',
            data=json.dumps({"title": "", "content": "", "user_id": 1}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_post_no_json(self, client):
        """Test POST /api/posts returns 415 for no content type"""
        response = client.post('/api/posts/')
        assert response.status_code == 415

    def test_create_post_invalid_user_id(self, client):
        """Test POST /api/posts returns 404 for non-existent user_id"""
        response = client.post(
            '/api/posts/',
            data=json.dumps({
                "title": "Test Post",
                "content": "Test content",
                "user_id": 999
            }),
            content_type='application/json'
        )
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_update_post_success(self, client):
        """Test PUT /api/posts/<id> updates post successfully"""
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "user_id": 2
        }
        response = client.put(
            '/api/posts/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['content'] == update_data['content']
        assert data['user_id'] == update_data['user_id']
        assert data['id'] == 1

        # Verify post was actually updated
        post = data_store.get_post(1)
        assert post.title == update_data['title']
        assert post.content == update_data['content']
        assert post.user_id == update_data['user_id']

    def test_update_post_partial(self, client):
        """Test PUT /api/posts/<id> with partial data"""
        update_data = {"title": "Partially Updated Title"}
        response = client.put(
            '/api/posts/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        # Original content unchanged
        assert data['content'] == "This is the content of the first post"
        assert data['user_id'] == 1  # Original user_id unchanged

    def test_update_post_not_found(self, client):
        """Test PUT /api/posts/<id> returns 404 for non-existent post"""
        response = client.put(
            '/api/posts/999',
            data=json.dumps({"title": "Updated"}),
            content_type='application/json'
        )
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "Post not found"

    def test_update_post_no_json(self, client):
        """Test PUT /api/posts/<id> returns 415 for no content type"""
        response = client.put('/api/posts/1')
        assert response.status_code == 415

    def test_update_post_invalid_user_id(self, client):
        """Test PUT /api/posts/<id> returns 404 for non-existent user_id"""
        response = client.put(
            '/api/posts/1',
            data=json.dumps({"user_id": 999}),
            content_type='application/json'
        )
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_delete_post_success(self, client):
        """Test DELETE /api/posts/<id> deletes post successfully"""
        response = client.delete('/api/posts/1')
        assert response.status_code == 204
        assert response.data == b''

        # Verify post was actually deleted
        post = data_store.get_post(1)
        assert post is None

    def test_delete_post_not_found(self, client):
        """Test DELETE /api/posts/<id> returns 404 for non-existent post"""
        response = client.delete('/api/posts/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "Post not found"

    def test_get_posts_by_user_success(self, client):
        """Test GET /api/posts/user/<user_id> returns user's posts"""
        response = client.get('/api/posts/user/1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2  # User 1 has 2 posts in sample data
        assert all(post['user_id'] == 1 for post in data)

    def test_get_posts_by_user_not_found(self, client):
        """Test GET /api/posts/user/<user_id> returns 404 for non-existent user"""
        response = client.get('/api/posts/user/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_get_posts_by_user_empty(self, client):
        """Test GET /api/posts/user/<user_id> returns empty list for user with no posts"""
        # Create a new user with no posts
        new_user = data_store.create_user(
            "No Posts User", "noposts@example.com")

        response = client.get(f'/api/posts/user/{new_user.id}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
