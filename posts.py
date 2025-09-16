from flask import Blueprint, jsonify, request
from data_store import data_store

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')


@posts_bp.route('/', methods=['GET'])
def get_posts():
    """Get all posts"""
    posts = data_store.get_all_posts()
    return jsonify([post.to_dict() for post in posts])


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single post by ID"""
    post = data_store.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict())


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

    new_post = data_store.create_post(
        data["title"], data["content"], data["user_id"])
    if not new_post:
        return jsonify({"error": "User not found"}), 404

    return jsonify(new_post.to_dict()), 201


@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post"""
    post = data_store.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    updated_post = data_store.update_post(
        post_id,
        title=data.get('title'),
        content=data.get('content'),
        user_id=data.get('user_id')
    )

    if not updated_post:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated_post.to_dict())


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    if not data_store.delete_post(post_id):
        return jsonify({"error": "Post not found"}), 404
    return '', 204


@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    """Get all posts by a specific user"""
    if not data_store.user_exists(user_id):
        return jsonify({"error": "User not found"}), 404

    user_posts = data_store.get_posts_by_user(user_id)
    return jsonify([post.to_dict() for post in user_posts])
