from data_store import data_store
import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAPIRequirements:
    """Test cases to verify all API requirements are met"""

    def test_users_get_all_returns_list_with_required_attributes(self, client):
        """Test GET /users returns list with id, name, email attributes"""
        response = client.get('/api/users/')
        assert response.status_code == 200

        users = json.loads(response.data)
        assert isinstance(users, list), "Response should be a list"
        assert len(users) >= 2, "Should have at least 2 sample users"

        for user in users:
            assert 'id' in user, "Each user should have an id attribute"
            assert 'name' in user, "Each user should have a name attribute"
            assert 'email' in user, "Each user should have an email attribute"
            assert isinstance(user['id'], int), "User id should be an integer"
            assert isinstance(
                user['name'], str), "User name should be a string"
            assert isinstance(
                user['email'], str), "User email should be a string"

    def test_users_post_creates_user_with_unique_id(self, client):
        """Test POST /users creates new user with unique server-assigned id"""
        new_user_data = {"name": "Requirements Test User",
                         "email": "requirements@example.com"}

        response = client.post('/api/users/',
                               data=json.dumps(new_user_data),
                               content_type='application/json')
        assert response.status_code == 201

        created_user = json.loads(response.data)
        assert 'id' in created_user, "Created user should have an id"
        assert isinstance(created_user['id'],
                          int), "User id should be an integer"
        assert created_user['name'] == new_user_data['name'], "Name should match request"
        assert created_user['email'] == new_user_data['email'], "Email should match request"

        # Verify user was actually created in data store
        user = data_store.get_user(created_user['id'])
        assert user is not None, "User should exist in data store"
        assert user.name == new_user_data['name'], "User name should be stored correctly"

    def test_users_get_by_id_returns_user_or_404(self, client):
        """Test GET /users/{id} returns user in JSON format or 404"""
        # Test with existing user
        response = client.get('/api/users/1')
        assert response.status_code == 200

        user = json.loads(response.data)
        assert user['id'] == 1, "User id should match requested id"
        assert 'name' in user and 'email' in user, "User should have name and email"

        # Test with non-existent user
        response = client.get('/api/users/99999')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert 'error' in error, "Error response should contain error message"
        assert error['error'] == "User not found", "Error message should be descriptive"

    def test_users_put_updates_user_or_404(self, client):
        """Test PUT /users/{id} updates user and returns updated user or 404"""
        # Test updating existing user
        update_data = {"name": "Updated Requirements User",
                       "email": "updated@example.com"}

        response = client.put('/api/users/1',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 200

        updated_user = json.loads(response.data)
        assert updated_user['name'] == update_data['name'], "Name should be updated"
        assert updated_user['email'] == update_data['email'], "Email should be updated"
        assert updated_user['id'] == 1, "User id should remain the same"

        # Test with non-existent user
        response = client.put('/api/users/99999',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert error['error'] == "User not found", "Should return 404 for non-existent user"

    def test_users_delete_returns_204_or_404(self, client):
        """Test DELETE /users/{id} returns 204 status code or 404"""
        # Create a user to delete
        new_user_data = {"name": "Delete Test User",
                         "email": "delete@example.com"}
        response = client.post('/api/users/',
                               data=json.dumps(new_user_data),
                               content_type='application/json')
        created_user = json.loads(response.data)
        user_id = created_user['id']

        # Test deleting existing user
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 204, "Should return 204 status code"
        assert response.data == b'', "Response body should be empty"

        # Verify user was actually deleted
        user = data_store.get_user(user_id)
        assert user is None, "User should be deleted from data store"

        # Test deleting non-existent user
        response = client.delete('/api/users/99999')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert error['error'] == "User not found", "Should return 404 for non-existent user"

    def test_posts_get_all_returns_list_with_required_attributes(self, client):
        """Test GET /posts returns list with id, title, content, user_id attributes"""
        response = client.get('/api/posts/')
        assert response.status_code == 200

        posts = json.loads(response.data)
        assert isinstance(posts, list), "Response should be a list"
        assert len(posts) >= 3, "Should have at least 3 sample posts"

        for post in posts:
            assert 'id' in post, "Each post should have an id attribute"
            assert 'title' in post, "Each post should have a title attribute"
            assert 'content' in post, "Each post should have a content attribute"
            assert 'user_id' in post, "Each post should have a user_id attribute"
            assert isinstance(post['id'], int), "Post id should be an integer"
            assert isinstance(
                post['title'], str), "Post title should be a string"
            assert isinstance(
                post['content'], str), "Post content should be a string"
            assert isinstance(
                post['user_id'], int), "Post user_id should be an integer"

    def test_posts_post_creates_post_with_unique_id_and_validates_user_id(self, client):
        """Test POST /posts creates post with unique id and validates user_id"""
        new_post_data = {"title": "Requirements Test Post",
                         "content": "Test content", "user_id": 1}

        response = client.post('/api/posts/',
                               data=json.dumps(new_post_data),
                               content_type='application/json')
        assert response.status_code == 201

        created_post = json.loads(response.data)
        assert 'id' in created_post, "Created post should have an id"
        assert isinstance(created_post['id'],
                          int), "Post id should be an integer"
        assert created_post['title'] == new_post_data['title'], "Title should match request"
        assert created_post['content'] == new_post_data['content'], "Content should match request"
        assert created_post['user_id'] == new_post_data['user_id'], "User_id should match request"

        # Verify post was actually created in data store
        post = data_store.get_post(created_post['id'])
        assert post is not None, "Post should exist in data store"
        assert post.title == new_post_data['title'], "Post title should be stored correctly"

    def test_posts_post_returns_404_for_invalid_user_id(self, client):
        """Test POST /posts returns 404 error for invalid user_id"""
        invalid_post_data = {"title": "Invalid Post",
                             "content": "Content", "user_id": 99999}

        response = client.post('/api/posts/',
                               data=json.dumps(invalid_post_data),
                               content_type='application/json')
        assert response.status_code == 404, "Should return 404 for invalid user_id"

        error = json.loads(response.data)
        assert error['error'] == "User not found", "Should return descriptive error message"

    def test_posts_get_by_id_returns_post_or_404(self, client):
        """Test GET /posts/{id} returns post in JSON format or 404"""
        # Test with existing post
        response = client.get('/api/posts/1')
        assert response.status_code == 200

        post = json.loads(response.data)
        assert post['id'] == 1, "Post id should match requested id"
        assert 'title' in post and 'content' in post and 'user_id' in post, "Post should have all required attributes"

        # Test with non-existent post
        response = client.get('/api/posts/99999')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert error['error'] == "Post not found", "Should return descriptive error message"

    def test_posts_put_updates_post_or_404(self, client):
        """Test PUT /posts/{id} updates post and returns updated post or 404"""
        # Test updating existing post
        update_data = {"title": "Updated Requirements Post",
                       "content": "Updated content", "user_id": 2}

        response = client.put('/api/posts/1',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 200

        updated_post = json.loads(response.data)
        assert updated_post['title'] == update_data['title'], "Title should be updated"
        assert updated_post['content'] == update_data['content'], "Content should be updated"
        assert updated_post['user_id'] == update_data['user_id'], "User_id should be updated"
        assert updated_post['id'] == 1, "Post id should remain the same"

        # Test with non-existent post
        response = client.put('/api/posts/99999',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert error['error'] == "Post not found", "Should return 404 for non-existent post"

    def test_posts_put_returns_404_for_invalid_user_id(self, client):
        """Test PUT /posts/{id} returns 404 for invalid user_id"""
        invalid_update = {"title": "Updated",
                          "content": "Content", "user_id": 99999}

        response = client.put('/api/posts/1',
                              data=json.dumps(invalid_update),
                              content_type='application/json')
        assert response.status_code == 404, "Should return 404 for invalid user_id"

        error = json.loads(response.data)
        assert error['error'] == "User not found", "Should return descriptive error message"

    def test_posts_delete_returns_204_or_404(self, client):
        """Test DELETE /posts/{id} returns 204 status code or 404"""
        # Create a post to delete
        new_post_data = {"title": "Delete Test Post",
                         "content": "Test content", "user_id": 1}
        response = client.post('/api/posts/',
                               data=json.dumps(new_post_data),
                               content_type='application/json')
        created_post = json.loads(response.data)
        post_id = created_post['id']

        # Test deleting existing post
        response = client.delete(f'/api/posts/{post_id}')
        assert response.status_code == 204, "Should return 204 status code"
        assert response.data == b'', "Response body should be empty"

        # Verify post was actually deleted
        post = data_store.get_post(post_id)
        assert post is None, "Post should be deleted from data store"

        # Test deleting non-existent post
        response = client.delete('/api/posts/99999')
        assert response.status_code == 404

        error = json.loads(response.data)
        assert error['error'] == "Post not found", "Should return 404 for non-existent post"

    def test_requirements_summary(self, client):
        """Summary test to verify all requirements are met"""
        # This test serves as a summary and final verification
        requirements_met = {
            "users_get_all": False,
            "users_post_create": False,
            "users_get_by_id": False,
            "users_put_update": False,
            "users_delete": False,
            "posts_get_all": False,
            "posts_post_create": False,
            "posts_post_validate_user_id": False,
            "posts_get_by_id": False,
            "posts_put_update": False,
            "posts_put_validate_user_id": False,
            "posts_delete": False
        }

        # Test users endpoints
        response = client.get('/api/users/')
        if response.status_code == 200:
            users = json.loads(response.data)
            if isinstance(users, list) and all('id' in u and 'name' in u and 'email' in u for u in users):
                requirements_met["users_get_all"] = True

        response = client.post('/api/users/',
                               data=json.dumps(
                                   {"name": "Test", "email": "test@test.com"}),
                               content_type='application/json')
        if response.status_code == 201:
            user = json.loads(response.data)
            if 'id' in user and isinstance(user['id'], int):
                requirements_met["users_post_create"] = True

        response = client.get('/api/users/1')
        if response.status_code == 200:
            requirements_met["users_get_by_id"] = True

        response = client.put('/api/users/1',
                              data=json.dumps({"name": "Updated"}),
                              content_type='application/json')
        if response.status_code == 200:
            requirements_met["users_put_update"] = True

        response = client.delete('/api/users/99999')
        if response.status_code == 404:
            requirements_met["users_delete"] = True

        # Test posts endpoints
        response = client.get('/api/posts/')
        if response.status_code == 200:
            posts = json.loads(response.data)
            if isinstance(posts, list) and all('id' in p and 'title' in p and 'content' in p and 'user_id' in p for p in posts):
                requirements_met["posts_get_all"] = True

        response = client.post('/api/posts/',
                               data=json.dumps(
                                   {"title": "Test", "content": "Content", "user_id": 1}),
                               content_type='application/json')
        if response.status_code == 201:
            post = json.loads(response.data)
            if 'id' in post and isinstance(post['id'], int):
                requirements_met["posts_post_create"] = True

        response = client.post('/api/posts/',
                               data=json.dumps(
                                   {"title": "Test", "content": "Content", "user_id": 99999}),
                               content_type='application/json')
        if response.status_code == 404:
            requirements_met["posts_post_validate_user_id"] = True

        response = client.get('/api/posts/1')
        if response.status_code == 200:
            requirements_met["posts_get_by_id"] = True

        response = client.put('/api/posts/1',
                              data=json.dumps({"title": "Updated"}),
                              content_type='application/json')
        if response.status_code == 200:
            requirements_met["posts_put_update"] = True

        response = client.put('/api/posts/1',
                              data=json.dumps({"user_id": 99999}),
                              content_type='application/json')
        if response.status_code == 404:
            requirements_met["posts_put_validate_user_id"] = True

        response = client.delete('/api/posts/99999')
        if response.status_code == 404:
            requirements_met["posts_delete"] = True

        # Verify all requirements are met
        failed_requirements = [req for req,
                               met in requirements_met.items() if not met]
        assert len(
            failed_requirements) == 0, f"Failed requirements: {failed_requirements}"

        print(
            f"\n✅ All {len(requirements_met)} requirements verified successfully!")
        for req, met in requirements_met.items():
            status = "✅" if met else "❌"
            print(f"  {status} {req}")
