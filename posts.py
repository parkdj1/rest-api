from flask import Blueprint, jsonify, request
from users import users_data

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

# Sample data for demonstration
posts_data = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post", "user_id": 1},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post", "user_id": 2},
    {"id": 3, "title": "Third Post", "content": "This is the content of the third post", "user_id": 1}
]

def validate_user_exists(user_id):
    """Helper function to validate if a user exists"""
    return any(user["id"] == user_id for user in users_data)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    """Get all posts"""
    return jsonify(posts_data)

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single post by ID"""
    post = next((post for post in posts_data if post["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)

@posts_bp.route('/', methods=['POST'])
def create_post():
    """Create a new post with user ID validation"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    required_fields = ['title', 'content', 'user_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Validate user_id exists
    if not validate_user_exists(data['user_id']):
        return jsonify({"error": "User not found"}), 404
    
    new_post = {
        "id": max([post["id"] for post in posts_data], default=0) + 1,
        "title": data["title"],
        "content": data["content"],
        "user_id": data["user_id"]
    }
    
    posts_data.append(new_post)
    return jsonify(new_post), 201

@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post"""
    post = next((post for post in posts_data if post["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Validate user_id if it's being updated
    if 'user_id' in data and data['user_id'] != post['user_id']:
        if not validate_user_exists(data['user_id']):
            return jsonify({"error": "User not found"}), 404
    
    # Update post fields
    for field in ['title', 'content', 'user_id']:
        if field in data:
            post[field] = data[field]
    
    return jsonify(post)

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    post = next((post for post in posts_data if post["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    posts_data.remove(post)
    return '', 204

@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    """Get all posts by a specific user"""
    if not validate_user_exists(user_id):
        return jsonify({"error": "User not found"}), 404
    
    user_posts = [post for post in posts_data if post["user_id"] == user_id]
    return jsonify(user_posts)
