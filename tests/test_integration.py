from data_store import data_store
import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestIntegration:
    """Integration tests for the complete API workflow"""

    def test_complete_user_workflow(self, client):
        """Test complete user CRUD workflow"""
        # 1. Get initial users
        response = client.get('/api/users/')
        assert response.status_code == 200
        initial_users = json.loads(response.data)
        initial_count = len(initial_users)

        # 2. Create a new user
        new_user_data = {
            "name": "Integration Test User",
            "email": "integration@example.com"
        }
        response = client.post(
            '/api/users/',
            data=json.dumps(new_user_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        created_user = json.loads(response.data)
        user_id = created_user['id']

        # 3. Verify user was created
        response = client.get(f'/api/users/{user_id}')
        assert response.status_code == 200
        retrieved_user = json.loads(response.data)
        assert retrieved_user['name'] == new_user_data['name']
        assert retrieved_user['email'] == new_user_data['email']

        # 4. Update the user
        update_data = {
            "name": "Updated Integration User",
            "email": "updated.integration@example.com"
        }
        response = client.put(
            f'/api/users/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        updated_user = json.loads(response.data)
        assert updated_user['name'] == update_data['name']
        assert updated_user['email'] == update_data['email']

        # 5. Verify total user count increased
        response = client.get('/api/users/')
        assert response.status_code == 200
        final_users = json.loads(response.data)
        assert len(final_users) == initial_count + 1

        # 6. Delete the user
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 204

        # 7. Verify user was deleted
        response = client.get(f'/api/users/{user_id}')
        assert response.status_code == 404

        # 8. Verify total user count is back to initial
        response = client.get('/api/users/')
        assert response.status_code == 200
        final_users = json.loads(response.data)
        assert len(final_users) == initial_count

    def test_complete_post_workflow(self, client):
        """Test complete post CRUD workflow"""
        # 1. Get initial posts
        response = client.get('/api/posts/')
        assert response.status_code == 200
        initial_posts = json.loads(response.data)
        initial_count = len(initial_posts)

        # 2. Create a new post
        new_post_data = {
            "title": "Integration Test Post",
            "content": "This is an integration test post",
            "user_id": 1
        }
        response = client.post(
            '/api/posts/',
            data=json.dumps(new_post_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        created_post = json.loads(response.data)
        post_id = created_post['id']

        # 3. Verify post was created
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 200
        retrieved_post = json.loads(response.data)
        assert retrieved_post['title'] == new_post_data['title']
        assert retrieved_post['content'] == new_post_data['content']
        assert retrieved_post['user_id'] == new_post_data['user_id']

        # 4. Update the post
        update_data = {
            "title": "Updated Integration Post",
            "content": "This is an updated integration test post",
            "user_id": 2
        }
        response = client.put(
            f'/api/posts/{post_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        updated_post = json.loads(response.data)
        assert updated_post['title'] == update_data['title']
        assert updated_post['content'] == update_data['content']
        assert updated_post['user_id'] == update_data['user_id']

        # 5. Verify total post count increased
        response = client.get('/api/posts/')
        assert response.status_code == 200
        final_posts = json.loads(response.data)
        assert len(final_posts) == initial_count + 1

        # 6. Delete the post
        response = client.delete(f'/api/posts/{post_id}')
        assert response.status_code == 204

        # 7. Verify post was deleted
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 404

        # 8. Verify total post count is back to initial
        response = client.get('/api/posts/')
        assert response.status_code == 200
        final_posts = json.loads(response.data)
        assert len(final_posts) == initial_count

    def test_user_post_relationship(self, client):
        """Test the relationship between users and posts"""
        # 1. Create a new user
        new_user_data = {
            "name": "Post Owner",
            "email": "postowner@example.com"
        }
        response = client.post(
            '/api/users/',
            data=json.dumps(new_user_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        user = json.loads(response.data)
        user_id = user['id']

        # 2. Create posts for this user
        posts_data = [
            {
                "title": "User's First Post",
                "content": "Content of first post",
                "user_id": user_id
            },
            {
                "title": "User's Second Post",
                "content": "Content of second post",
                "user_id": user_id
            }
        ]

        created_posts = []
        for post_data in posts_data:
            response = client.post(
                '/api/posts/',
                data=json.dumps(post_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_posts.append(json.loads(response.data))

        # 3. Verify user's posts
        response = client.get(f'/api/posts/user/{user_id}')
        assert response.status_code == 200
        user_posts = json.loads(response.data)
        assert len(user_posts) == 2

        # 4. Delete user and verify posts are also deleted
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 204

        # 5. Verify user's posts were deleted
        response = client.get(f'/api/posts/user/{user_id}')
        assert response.status_code == 404

        # 6. Verify individual posts are deleted
        for post in created_posts:
            response = client.get(f'/api/posts/{post["id"]}')
            assert response.status_code == 404

    def test_error_handling_workflow(self, client):
        """Test error handling across the API"""
        # 1. Test creating post with invalid user_id
        response = client.post(
            '/api/posts/',
            data=json.dumps({
                "title": "Invalid Post",
                "content": "This should fail",
                "user_id": 999
            }),
            content_type='application/json'
        )
        assert response.status_code == 404

        # 2. Test updating non-existent user
        response = client.put(
            '/api/users/999',
            data=json.dumps({"name": "Updated"}),
            content_type='application/json'
        )
        assert response.status_code == 404

        # 3. Test updating post with invalid user_id
        response = client.put(
            '/api/posts/1',
            data=json.dumps({"user_id": 999}),
            content_type='application/json'
        )
        assert response.status_code == 404

        # 4. Test creating user with duplicate email
        response = client.post(
            '/api/users/',
            data=json.dumps({
                "name": "Duplicate Email User",
                "email": "john@example.com"  # This email already exists
            }),
            content_type='application/json'
        )
        assert response.status_code == 409

        # 5. Test malformed JSON
        response = client.post(
            '/api/users/',
            data="invalid json",
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_data_consistency(self, client):
        """Test data consistency across operations"""
        # 1. Get initial state
        response = client.get('/api/users/')
        initial_users = json.loads(response.data)

        response = client.get('/api/posts/')
        initial_posts = json.loads(response.data)

        # 2. Create user and posts
        user_data = {"name": "Consistency User",
                     "email": "consistency@example.com"}
        response = client.post(
            '/api/users/', data=json.dumps(user_data), content_type='application/json')
        user = json.loads(response.data)

        post_data = {"title": "Consistency Post",
                     "content": "Content", "user_id": user['id']}
        response = client.post(
            '/api/posts/', data=json.dumps(post_data), content_type='application/json')
        post = json.loads(response.data)

        # 3. Verify data consistency
        response = client.get(f'/api/users/{user["id"]}')
        assert response.status_code == 200

        response = client.get(f'/api/posts/{post["id"]}')
        assert response.status_code == 200

        response = client.get(f'/api/posts/user/{user["id"]}')
        user_posts = json.loads(response.data)
        assert len(user_posts) == 1
        assert user_posts[0]['id'] == post['id']

        # 4. Clean up
        client.delete(f'/api/users/{user["id"]}')

        # 5. Verify cleanup
        response = client.get('/api/users/')
        final_users = json.loads(response.data)
        assert len(final_users) == len(initial_users)

        response = client.get('/api/posts/')
        final_posts = json.loads(response.data)
        assert len(final_posts) == len(initial_posts)
