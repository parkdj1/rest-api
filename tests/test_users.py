from data_store import data_store
import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUsersEndpoints:
    """Test cases for /api/users endpoints"""

    def test_get_all_users_success(self, client):
        """Test GET /api/users returns all users"""
        response = client.get('/api/users/')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2  # Sample data has 2 users
        assert data[0]['name'] == "John Doe"
        assert data[1]['name'] == "Jane Smith"

    def test_get_user_success(self, client):
        """Test GET /api/users/<id> returns specific user"""
        response = client.get('/api/users/1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['name'] == "John Doe"
        assert data['email'] == "john@example.com"

    def test_get_user_not_found(self, client):
        """Test GET /api/users/<id> returns 404 for non-existent user"""
        response = client.get('/api/users/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_create_user_success(self, client, sample_user_data):
        """Test POST /api/users creates new user successfully"""
        response = client.post(
            '/api/users/',
            data=json.dumps(sample_user_data),
            content_type='application/json'
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['name'] == sample_user_data['name']
        assert data['email'] == sample_user_data['email']
        assert 'id' in data

        # Verify user was actually created
        user = data_store.get_user(data['id'])
        assert user is not None
        assert user.name == sample_user_data['name']

    def test_create_user_missing_data(self, client):
        """Test POST /api/users returns 400 for missing required fields"""
        # Missing name
        response = client.post(
            '/api/users/',
            data=json.dumps({"email": "test@example.com"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Validation failed" in data['error']
        assert 'name' in data['details']

        # Missing email
        response = client.post(
            '/api/users/',
            data=json.dumps({"name": "Test User"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Validation failed" in data['error']
        assert 'email' in data['details']

    def test_create_user_empty_data(self, client):
        """Test POST /api/users returns 400 for empty data"""
        response = client.post(
            '/api/users/',
            data=json.dumps({"name": "", "email": ""}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_user_no_json(self, client):
        """Test POST /api/users returns 415 for no content type"""
        response = client.post('/api/users/')
        assert response.status_code == 415

    def test_create_user_duplicate_email(self, client):
        """Test POST /api/users returns 409 for duplicate email"""
        response = client.post(
            '/api/users/',
            data=json.dumps(
                {"name": "Another User", "email": "john@example.com"}),
            content_type='application/json'
        )
        assert response.status_code == 409

        data = json.loads(response.data)
        assert data['error'] == "Email already exists"

    def test_update_user_success(self, client):
        """Test PUT /api/users/<id> updates user successfully"""
        update_data = {"name": "Updated Name", "email": "updated@example.com"}
        response = client.put(
            '/api/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['name'] == update_data['name']
        assert data['email'] == update_data['email']
        assert data['id'] == 1

        # Verify user was actually updated
        user = data_store.get_user(1)
        assert user.name == update_data['name']
        assert user.email == update_data['email']

    def test_update_user_partial(self, client):
        """Test PUT /api/users/<id> with partial data"""
        update_data = {"name": "Partially Updated"}
        response = client.put(
            '/api/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['name'] == update_data['name']
        assert data['email'] == "john@example.com"  # Original email unchanged

    def test_update_user_not_found(self, client):
        """Test PUT /api/users/<id> returns 404 for non-existent user"""
        response = client.put(
            '/api/users/999',
            data=json.dumps({"name": "Updated"}),
            content_type='application/json'
        )
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_update_user_no_json(self, client):
        """Test PUT /api/users/<id> returns 415 for no content type"""
        response = client.put('/api/users/1')
        assert response.status_code == 415

    def test_update_user_duplicate_email(self, client):
        """Test PUT /api/users/<id> returns 409 for duplicate email"""
        response = client.put(
            '/api/users/1',
            data=json.dumps({"email": "jane@example.com"}),
            content_type='application/json'
        )
        assert response.status_code == 409

        data = json.loads(response.data)
        assert data['error'] == "Email already exists"

    def test_delete_user_success(self, client):
        """Test DELETE /api/users/<id> deletes user successfully"""
        response = client.delete('/api/users/1')
        assert response.status_code == 204
        assert response.data == b''

        # Verify user was actually deleted
        user = data_store.get_user(1)
        assert user is None

    def test_delete_user_not_found(self, client):
        """Test DELETE /api/users/<id> returns 404 for non-existent user"""
        response = client.delete('/api/users/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error'] == "User not found"

    def test_delete_user_cascades_to_posts(self, client):
        """Test DELETE /api/users/<id> also deletes user's posts"""
        # Verify user has posts
        user_posts = data_store.get_posts_by_user(1)
        assert len(user_posts) > 0

        # Delete user
        response = client.delete('/api/users/1')
        assert response.status_code == 204

        # Verify user's posts were also deleted
        user_posts_after = data_store.get_posts_by_user(1)
        assert len(user_posts_after) == 0
